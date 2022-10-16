
function fetchSuggestions(url) {
    fetch(url)
    .then((response) => {
        return response.json
    })
    .then((data) => {
        console.log(data.value);
    })
}

function test() {
    return 2
}
let color = "#3AA757"

chrome.runtime.onInstalled.addListener(()=> {
    chrome.storage.sync.set({color})
    console.log(test())
})

chrome.tabs.query({active: true, lastFocusedWindow: true}, tabs => {
    let url = tabs[0].url;
    //fetchSuggestions(url);
});