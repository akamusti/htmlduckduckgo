"use strict";

chrome.omnibox.setDefaultSuggestion({
  description: "Search DuckDuckGo HTML: %s",
});

chrome.omnibox.onInputEntered.addListener((text, disposition) => {
  const url = `https://html.duckduckgo.com/html/?q=${encodeURIComponent(text)}`;

  if (disposition === "currentTab") {
    chrome.tabs.query({ active: true, lastFocusedWindow: true }, (tabs) => {
      const activeTab = tabs[0];
      if (activeTab?.id === undefined) {
        console.error("Could not find the active tab for the DuckDuckGo search.");
        return;
      }

      chrome.tabs.update(activeTab.id, { url }, () => {
        if (chrome.runtime.lastError) {
          console.error("Could not navigate the active tab:", chrome.runtime.lastError.message);
        }
      });
    });
    return;
  }

  chrome.tabs.create({ url, active: disposition !== "newBackgroundTab" }, () => {
    if (chrome.runtime.lastError) {
      console.error("Could not open the DuckDuckGo search:", chrome.runtime.lastError.message);
    }
  });
});
