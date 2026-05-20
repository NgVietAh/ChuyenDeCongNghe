*** Settings ***
Documentation       Facebook Personal Post Crawler
...                 Crawl posts from a Facebook user's profile page
...                 including post content, timestamps, and image URLs.
...
...                 Usage:
...                 robot --variable EMAIL:your_email --variable PASSWORD:your_pass
...                 --variable PROFILE_URL:https://www.facebook.com/username
...                 tasks/crawl_facebook_posts.robot

Library             SeleniumLibrary
Library             Collections
Library             OperatingSystem
Library             ../libraries/FacebookCrawler.py
Library             ../libraries/DataProcessor.py
Resource            ../resources/facebook_keywords.resource
Resource            ../resources/variables.resource

Suite Setup         Setup Crawl Session
Suite Teardown      Teardown Crawl Session

*** Variables ***
# These can be overridden via command line:
# robot --variable EMAIL:xxx --variable PASSWORD:xxx --variable PROFILE_URL:xxx
${EMAIL}            ${EMPTY}
${PASSWORD}         ${EMPTY}
${PROFILE_URL}      ${EMPTY}
${MAX_POSTS}        20
${HEADLESS}         ${FALSE}
${CONFIG_PATH}      ${CURDIR}/../config/config.yaml

*** Test Cases ***
Crawl Facebook Personal Posts
    [Documentation]    Main task: Crawl posts from a Facebook profile
    [Tags]    crawl    facebook    posts

    # Step 1: Login to Facebook
    Login To Facebook Account

    # Step 2: Navigate to user profile
    Navigate To User Profile

    # Step 3: Scroll to load posts
    Load Posts By Scrolling

    # Step 4: Extract data from all posts
    Extract All Post Data

    # Step 5: Download images (if enabled)
    Download Post Images

    # Step 6: Save results
    ${output_file}=    Save Crawl Results
    Log    Results saved to: ${output_file}

    # Step 7: Print summary
    Print Crawl Summary

*** Keywords ***
Setup Crawl Session
    [Documentation]    Initialize crawler and open browser
    Initialize Crawler    ${CONFIG_PATH}

    # Override config with command line variables if provided
    ${email}=    Get Credentials Email
    ${password}=    Get Credentials Password
    ${profile}=    Get Profile URL Value

    Set Suite Variable    ${FB_EMAIL}    ${email}
    Set Suite Variable    ${FB_PASSWORD}    ${password}
    Set Suite Variable    ${FB_PROFILE_URL}    ${profile}

    Open Facebook Browser    headless=${HEADLESS}

Teardown Crawl Session
    [Documentation]    Cleanup after crawling
    Cleanup Browser

Get Credentials Email
    [Documentation]    Get email from command line or config
    IF    '${EMAIL}' != '${EMPTY}'
        RETURN    ${EMAIL}
    END
    ${email}=    Get Config Value    facebook    email
    RETURN    ${email}

Get Credentials Password
    [Documentation]    Get password from command line or config
    IF    '${PASSWORD}' != '${EMPTY}'
        RETURN    ${PASSWORD}
    END
    ${password}=    Get Config Value    facebook    password
    RETURN    ${password}

Get Profile URL Value
    [Documentation]    Get profile URL from command line or config
    IF    '${PROFILE_URL}' != '${EMPTY}'
        RETURN    ${PROFILE_URL}
    END
    ${url}=    Get Config Value    facebook    profile_url
    RETURN    ${url}

Login To Facebook Account
    [Documentation]    Login to Facebook with credentials
    Log    Logging in to Facebook...
    Login To Facebook    ${FB_EMAIL}    ${FB_PASSWORD}
    Log    Login successful!

Navigate To User Profile
    [Documentation]    Navigate to the target user's profile
    Log    Navigating to profile: ${FB_PROFILE_URL}
    Navigate To Profile    ${FB_PROFILE_URL}
    Log    Profile page loaded

Load Posts By Scrolling
    [Documentation]    Scroll down to load posts
    ${max_scrolls}=    Get Config Value    crawler    max_scroll_attempts
    ${max_scrolls}=    Convert To Integer    ${max_scrolls}
    ${max_posts_config}=    Get Max Posts
    ${max_posts_int}=    Convert To Integer    ${MAX_POSTS}
    ${effective_max}=    Set Variable If    ${max_posts_int} > 0    ${max_posts_int}    ${max_posts_config}

    Log    Loading posts (max: ${effective_max}, max scrolls: ${max_scrolls})...
    Scroll And Load Posts    max_scrolls=${max_scrolls}    max_posts=${effective_max}

Extract All Post Data
    [Documentation]    Extract data from all loaded posts
    ${max_posts_int}=    Convert To Integer    ${MAX_POSTS}
    Log    Extracting post data (max: ${max_posts_int})...
    Crawl All Posts    max_posts=${max_posts_int}

    ${total}=    Get Total Posts
    Log    Extracted ${total} posts
    Should Be True    ${total} > 0
    ...    msg=No posts were extracted. The profile might be private or the page structure has changed.
