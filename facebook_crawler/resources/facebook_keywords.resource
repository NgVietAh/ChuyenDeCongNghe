*** Settings ***
Documentation       Custom keywords for Facebook crawling operations
Library             SeleniumLibrary
Library             Collections
Library             String
Library             OperatingSystem
Library             ../libraries/FacebookCrawler.py
Library             ../libraries/DataProcessor.py
Resource            variables.resource

*** Keywords ***
Initialize Crawler
    [Documentation]    Load config and initialize the crawler
    [Arguments]    ${config_path}=${CURDIR}/../config/config.yaml
    ${config}=    Load Config    ${config_path}
    Set Suite Variable    ${CONFIG}    ${config}
    Log    Configuration loaded successfully

Open Facebook Browser
    [Documentation]    Open browser and navigate to Facebook
    [Arguments]    ${browser}=${BROWSER}    ${headless}=${FALSE}
    ${chrome_options}=    Evaluate    sys.modules['selenium.webdriver'].ChromeOptions()    sys
    Call Method    ${chrome_options}    add_argument    --disable-notifications
    Call Method    ${chrome_options}    add_argument    --disable-infobars
    Call Method    ${chrome_options}    add_argument    --disable-extensions
    Call Method    ${chrome_options}    add_argument    --no-sandbox
    Call Method    ${chrome_options}    add_argument    --disable-dev-shm-usage
    Call Method    ${chrome_options}    add_argument    --lang=vi
    IF    ${headless}
        Call Method    ${chrome_options}    add_argument    --headless=new
    END
    Create Webdriver    Chrome    options=${chrome_options}
    Set Window Size    ${WINDOW_WIDTH}    ${WINDOW_HEIGHT}
    Set Selenium Timeout    ${DEFAULT_TIMEOUT}
    Set Selenium Implicit Wait    10s

Handle Cookie Consent
    [Documentation]    Accept cookie consent dialog if present
    ${status}=    Run Keyword And Return Status
    ...    Wait Until Element Is Visible    ${COOKIE_ACCEPT_BUTTON}    timeout=5s
    IF    ${status}
        Click Element    ${COOKIE_ACCEPT_BUTTON}
        Sleep    ${SHORT_WAIT}
    END

Login To Facebook
    [Documentation]    Login to Facebook with provided credentials
    [Arguments]    ${email}    ${password}
    Go To    ${LOGIN_URL}
    Sleep    ${SHORT_WAIT}

    Handle Cookie Consent

    Wait Until Element Is Visible    ${LOGIN_EMAIL_FIELD}    timeout=${DEFAULT_TIMEOUT}
    Input Text    ${LOGIN_EMAIL_FIELD}    ${email}
    Input Text    ${LOGIN_PASSWORD_FIELD}    ${password}
    Click Element    ${LOGIN_BUTTON}

    # Wait for login to complete
    Sleep    ${LONG_WAIT}

    # Verify login success by checking URL change
    ${current_url}=    Get Location
    Should Not Contain    ${current_url}    login
    ...    msg=Login failed. Please check your credentials.

    Log    Successfully logged in to Facebook

Navigate To Profile
    [Documentation]    Navigate to the target Facebook profile
    [Arguments]    ${profile_url}
    Go To    ${profile_url}
    Sleep    ${LONG_WAIT}

    # Wait for the main content to load
    Wait Until Element Is Visible    ${POSTS_CONTAINER}    timeout=${DEFAULT_TIMEOUT}
    Log    Navigated to profile: ${profile_url}

Scroll Page Down
    [Documentation]    Scroll the page down to load more posts
    Execute Javascript    window.scrollTo(0, document.body.scrollHeight);
    Sleep    ${SCROLL_PAUSE}

Get Current Scroll Height
    [Documentation]    Get current page scroll height
    ${height}=    Execute Javascript    return document.body.scrollHeight;
    RETURN    ${height}

Scroll And Load Posts
    [Documentation]    Scroll down the page to load all posts
    [Arguments]    ${max_scrolls}=50    ${max_posts}=20
    ${previous_height}=    Get Current Scroll Height
    ${scroll_count}=    Set Variable    0
    ${no_change_count}=    Set Variable    0

    WHILE    ${scroll_count} < ${max_scrolls}
        Scroll Page Down

        ${current_height}=    Get Current Scroll Height

        # Check if we have enough posts
        ${post_count}=    Get Element Count    ${POST_ELEMENTS}
        IF    ${max_posts} > 0 and ${post_count} >= ${max_posts}
            Log    Reached target post count: ${post_count}
            BREAK
        END

        # Check if page height changed (new content loaded)
        IF    '${current_height}' == '${previous_height}'
            ${no_change_count}=    Evaluate    ${no_change_count} + 1
            IF    ${no_change_count} >= 3
                Log    No new content loaded after 3 attempts. Stopping scroll.
                BREAK
            END
        ELSE
            ${no_change_count}=    Set Variable    0
        END

        ${previous_height}=    Set Variable    ${current_height}
        ${scroll_count}=    Evaluate    ${scroll_count} + 1
    END

    Log    Scrolling complete after ${scroll_count} scrolls

Extract Post Content
    [Documentation]    Extract text content from a post element
    [Arguments]    ${post_element}
    ${content}=    Set Variable    ${EMPTY}
    ${status}=    Run Keyword And Return Status
    ...    Set Variable    ${post_element}

    # Try multiple content selectors
    @{content_selectors}=    Create List
    ...    div[data-ad-preview='message']
    ...    div[data-ad-comet-preview='message']
    ...    div[dir='auto']

    FOR    ${selector}    IN    @{content_selectors}
        ${found}=    Run Keyword And Return Status
        ...    Find Child Element And Get Text    ${post_element}    ${selector}
        IF    ${found}
            ${content}=    Find Child Element And Get Text    ${post_element}    ${selector}
            IF    '${content}' != '${EMPTY}'
                BREAK
            END
        END
    END

    ${content}=    Clean Post Content    ${content}
    RETURN    ${content}

Find Child Element And Get Text
    [Documentation]    Find a child element within a parent and get its text
    [Arguments]    ${parent}    ${css_selector}
    ${elements}=    Execute Javascript
    ...    return arguments[0].querySelectorAll('${css_selector}');
    ...    ARGUMENTS    ${parent}
    ${count}=    Execute Javascript
    ...    return arguments[0].querySelectorAll('${css_selector}').length;
    ...    ARGUMENTS    ${parent}

    IF    ${count} > 0
        ${text}=    Execute Javascript
        ...    var els = arguments[0].querySelectorAll('${css_selector}');
        ...    var texts = [];
        ...    for(var i=0; i < els.length; i++) {
        ...        var t = els[i].innerText || els[i].textContent;
        ...        if(t && t.trim()) texts.push(t.trim());
        ...    }
        ...    return texts.join(' ');
        ...    ARGUMENTS    ${parent}
        RETURN    ${text}
    END
    RETURN    ${EMPTY}

Extract Post Time
    [Documentation]    Extract timestamp from a post element
    [Arguments]    ${post_element}
    ${time_text}=    Set Variable    ${EMPTY}

    ${time_text}=    Execute Javascript
    ...    var el = arguments[0];
    ...    // Try to find time from aria-label on links
    ...    var links = el.querySelectorAll('a[href*="/posts/"], a[href*="permalink"], a[href*="/photo"]');
    ...    for(var i=0; i < links.length; i++) {
    ...        var ariaLabel = links[i].getAttribute('aria-label');
    ...        if(ariaLabel) return ariaLabel;
    ...        // Check child spans
    ...        var spans = links[i].querySelectorAll('span');
    ...        for(var j=0; j < spans.length; j++) {
    ...            var t = spans[j].innerText || spans[j].textContent;
    ...            if(t && t.trim()) return t.trim();
    ...        }
    ...    }
    ...    // Try abbr elements
    ...    var abbrs = el.querySelectorAll('abbr');
    ...    for(var i=0; i < abbrs.length; i++) {
    ...        var title = abbrs[i].getAttribute('title') || abbrs[i].getAttribute('data-utime');
    ...        if(title) return title;
    ...        var t = abbrs[i].innerText || abbrs[i].textContent;
    ...        if(t && t.trim()) return t.trim();
    ...    }
    ...    return '';
    ...    ARGUMENTS    ${post_element}

    ${time_text}=    Parse Facebook Time    ${time_text}
    RETURN    ${time_text}

Extract Post Images
    [Documentation]    Extract image URLs from a post element
    [Arguments]    ${post_element}
    ${image_urls}=    Execute Javascript
    ...    var el = arguments[0];
    ...    var urls = [];
    ...    var imgs = el.querySelectorAll('img');
    ...    for(var i=0; i < imgs.length; i++) {
    ...        var src = imgs[i].getAttribute('src') || '';
    ...        var dataSrc = imgs[i].getAttribute('data-src') || '';
    ...        var url = dataSrc || src;
    ...        if(url && url.startsWith('http')) {
    ...            // Skip small icons, emojis, and profile pictures
    ...            var width = imgs[i].naturalWidth || imgs[i].width || 0;
    ...            var height = imgs[i].naturalHeight || imgs[i].height || 0;
    ...            var isSmall = (width > 0 && width < 50) || (height > 0 && height < 50);
    ...            var isEmoji = url.includes('emoji') || url.includes('icon');
    ...            var isProfile = url.includes('profile') && (width < 100);
    ...            if(!isSmall && !isEmoji && !isProfile) {
    ...                urls.push(url);
    ...            }
    ...        }
    ...    }
    ...    // Remove duplicates
    ...    return [...new Set(urls)];
    ...    ARGUMENTS    ${post_element}

    RETURN    ${image_urls}

Extract Post Link
    [Documentation]    Extract permalink URL from a post element
    [Arguments]    ${post_element}
    ${post_url}=    Execute Javascript
    ...    var el = arguments[0];
    ...    var links = el.querySelectorAll('a[href*="/posts/"], a[href*="permalink"]');
    ...    if(links.length > 0) {
    ...        return links[0].href;
    ...    }
    ...    return '';
    ...    ARGUMENTS    ${post_element}
    RETURN    ${post_url}

Crawl Single Post
    [Documentation]    Crawl data from a single post element
    [Arguments]    ${post_element}    ${index}
    Log    Crawling post #${index}...

    ${content}=    Extract Post Content    ${post_element}
    ${post_time}=    Extract Post Time    ${post_element}
    ${image_urls}=    Extract Post Images    ${post_element}
    ${post_url}=    Extract Post Link    ${post_element}

    # Convert image URLs list to comma-separated string
    ${image_urls_str}=    Evaluate    ','.join($image_urls) if isinstance($image_urls, list) else str($image_urls)

    ${post}=    Add Post    ${content}    ${post_time}    ${image_urls_str}    ${post_url}

    ${img_count}=    Get Length    ${image_urls}
    Log    Post #${index}: Content length=${content.__len__()}, Time=${post_time}, Images=${img_count}

    RETURN    ${post}

Crawl All Posts
    [Documentation]    Crawl all visible posts on the profile page
    [Arguments]    ${max_posts}=20
    ${articles}=    Get WebElements    ${POST_ELEMENTS}
    ${total}=    Get Length    ${articles}

    ${limit}=    Set Variable If    ${max_posts} > 0    ${max_posts}    ${total}
    ${limit}=    Evaluate    min(${limit}, ${total})

    Log    Found ${total} post elements. Will crawl up to ${limit} posts.

    FOR    ${index}    IN RANGE    ${limit}
        ${post_element}=    Get From List    ${articles}    ${index}
        ${status}=    Run Keyword And Return Status
        ...    Crawl Single Post    ${post_element}    ${index + 1}
        IF    not ${status}
            Log    Warning: Failed to crawl post #${index + 1}. Skipping...    WARN
        END
    END

    ${crawled}=    Get Total Posts
    Log    Successfully crawled ${crawled} posts

Download Post Images
    [Documentation]    Download all images from crawled posts
    ${should_download}=    Should Download Images
    IF    ${should_download}
        ${total}=    Download All Images
        Log    Downloaded ${total} images
    ELSE
        Log    Image downloading is disabled in config
    END

Save Crawl Results
    [Documentation]    Save all crawled data to output file
    ${filepath}=    Save Results
    Log    Results saved to: ${filepath}
    RETURN    ${filepath}

Print Crawl Summary
    [Documentation]    Print a summary of the crawl results
    ${posts}=    Get Posts
    ${summary}=    Create Post Summary    ${posts}

    Log    ============================================
    Log    CRAWL SUMMARY
    Log    ============================================
    Log    Total posts crawled: ${summary}[total_posts]
    Log    Posts with content: ${summary}[posts_with_content]
    Log    Posts with images: ${summary}[posts_with_images]
    Log    Total images found: ${summary}[total_images]
    Log    ============================================

Cleanup Browser
    [Documentation]    Close browser and clean up
    Close All Browsers
    Log    Browser closed and cleanup complete
