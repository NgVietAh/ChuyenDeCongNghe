*** Settings ***
Documentation    Variables and configuration for Facebook Crawler

*** Variables ***
# =============================================
# Facebook Login Page Locators
# =============================================
${LOGIN_URL}                    https://www.facebook.com/
${LOGIN_EMAIL_FIELD}            id=email
${LOGIN_PASSWORD_FIELD}         id=pass
${LOGIN_BUTTON}                 xpath=//button[@name='login'] | //button[@data-testid='royal_login_button']
${COOKIE_ACCEPT_BUTTON}         xpath=//button[@data-cookiebanner='accept_button'] | //button[contains(text(),'Allow')] | //button[contains(text(),'Cho phép')] | //button[contains(text(),'Accept')]

# =============================================
# Facebook Profile Page Locators
# =============================================
# Main post feed container
${POSTS_CONTAINER}              xpath=//div[@role='main']

# Individual post elements - Facebook uses various structures
${POST_ELEMENTS}                xpath=//div[@role='article'] | //div[contains(@class,'userContentWrapper')]

# Post content text
${POST_CONTENT_XPATH}           .//div[@data-ad-preview='message'] | .//div[@data-ad-comet-preview='message'] | .//div[contains(@class,'xdj266r')]//span[contains(@class,'x193iq5w')] | .//div[@dir='auto']

# Post timestamp
${POST_TIME_XPATH}              .//a[contains(@href,'/posts/')] | .//a[contains(@href,'permalink')] | .//a[contains(@href,'/photo')] | .//span[contains(@class,'timestampContent')] | .//abbr

# Post images
${POST_IMAGE_XPATH}             .//img[contains(@class,'x1ey2m1c')] | .//img[contains(@class,'scaledImageFit')] | .//img[@data-visualcompletion='media-vc-image'] | .//div[contains(@class,'mtm')]//img

# Post link/permalink
${POST_LINK_XPATH}              .//a[contains(@href,'/posts/')] | .//a[contains(@href,'permalink')] | .//a[contains(@href,'/photo')]

# =============================================
# Timeouts and Delays
# =============================================
${DEFAULT_TIMEOUT}              30s
${SCROLL_PAUSE}                 3
${SHORT_WAIT}                   2
${LONG_WAIT}                    5

# =============================================
# Browser Settings
# =============================================
${BROWSER}                      chrome
${WINDOW_WIDTH}                 1920
${WINDOW_HEIGHT}                1080
