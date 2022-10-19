
const API = "http://localhost:5000/search?query="

function fetchSuggestions(url) {
    console.info(API + url);
    fetch(API + url)
    .then((response) => {
        return response.json();
    })
    .then((data) => {
        console.log(data);
        // chrome.action.setBadgeText({text :"TIP!"}, () => {});
        // chrome.action.setBadgeBackgroundColor({color :"#ffb366"}, () => {});

        chrome.tabs.query({active: true, lastFocusedWindow: true}, function(tabs) {
            chrome.tabs.sendMessage(tabs[0].id, data, function(response) {
            console.log(response.farewell);
            });
        });
    })

}

const filter = {url: [{hostSuffix: 'food.com', pathPrefix:'/recipe/'}]};

chrome.webNavigation.onBeforeNavigate.addListener(() => {

    console.info("Detected food.com recipe");
    chrome.tabs.query({active: true, lastFocusedWindow: true}, tabs => {
       let url = tabs[0].url;
        console.info(url);
        fetchSuggestions(url);
    });


    /*
    chrome.tabs.create({
        url: chrome.runtime.getURL('./popup.html'),
        active: false
    }, function(tab) {
        // After the tab has been created, open a window to inject the tab
        chrome.windows.create({
            tabId: tab.id,
            type: 'popup',
            focused: true
            // incognito, top, left, ...
        });
    });*/
  }, filter);
