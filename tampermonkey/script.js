// ==UserScript==
// @name         YTM Remote Control
// @namespace    http://tampermonkey.net/
// @version      1.0
// @description  Remote control YTM via local server
// @author       Gemini
// @match        *://music.youtube.com/*
// @icon         https://www.google.com/s2/favicons?sz=64&domain=youtube.com
// @grant        GM_xmlhttpRequest
// @connect      localhost
// @run-at       document-end
// ==/UserScript==

(function() {
    'use strict';
    console.log("Remote Script Running...");

    function poll() {
        GM_xmlhttpRequest({
            method: "GET",
            url: "http://localhost:3000/poll",
            onload: (res) => {
                const data = JSON.parse(res.responseText);
                if (data && data.videoId && data.title && data.action && data.artist) {
                    loadPage(data.title,data.artist,data.videoId,data.action);
                }
            }
        });
    }

    function loadPage(title,artist,videoId,action) {

    // 1. Find and open the search bar if it's closed
    const searchOpenButton = document.querySelector('ytmusic-search-box') ||
                             document.querySelector('tp-yt-paper-icon-button[aria-label="Search"]');

    if (searchOpenButton) {
        searchOpenButton.click();
    }

    // 2. Wait a moment for the animation/DOM to catch up
    setTimeout(() => {
        const searchInput = document.querySelector('input.ytmusic-search-box') ||
                           document.querySelector('#input.ytmusic-search-box') ||
                           document.querySelector('input#input');

        if (searchInput) {
            // 3. Focus and set the value
            searchInput.focus();
            searchInput.value = title + " " + artist;

            // 4. Force the app to "see" the new text
            searchInput.dispatchEvent(new Event('input', { bubbles: true }));
            searchInput.dispatchEvent(new Event('change', { bubbles: true }));

            // 5. Instead of pressing Enter, find the "Search" icon inside the bar and click it
            // This is usually the glass icon that appears once you start typing
            const searchSubmitButton = document.querySelector('.search-icon.ytmusic-search-box') ||
                                       document.querySelector('ytmusic-search-box [icon="search"]');

            if (searchSubmitButton) {
                searchSubmitButton.click();
                console.log("Search button clicked!");
            } else {
                // Fallback: If no button, try the "Enter" key again with a more complete event
                const opts = { bubbles: true, cancelable: true, key: 'Enter', code: 'Enter', keyCode: 13, which: 13 };
                searchInput.dispatchEvent(new KeyboardEvent('keydown', opts));
                searchInput.dispatchEvent(new KeyboardEvent('keypress', opts));
                searchInput.dispatchEvent(new KeyboardEvent('keyup', opts));
                console.log("Search button not found, tried full key sequence.");
            }
        }
    }, 300);
    setTimeout(() => {
        addToQueue(videoId, action);
    }, 1000);
}

function addToQueue(videoId, action) {
    console.log("adding");
    const actionLabel = action === 'next' ? 'play next' : 'add to queue';

    function tryAddToQueue() {
        // 1. Find the link for your video
        const videoLink = document.querySelector(`a[href*="${videoId}"]`);

        if (!videoLink) {
            console.log("Waiting for search results...");
            return false;
        }

        // 2. Find the Action Menu button near that link
        let container = videoLink.parentElement;
        let menuButton = null;
        for (let i = 0; i < 10; i++) {
            if (!container) break;
            menuButton = container.querySelector('button[aria-label="Action menu"]');
            if (menuButton) break;
            container = container.parentElement;
        }

        if (menuButton) {
            menuButton.click();

            // 3. Find the EXCLUSIVE "Add to queue" option
            setTimeout(() => {
                const menuOptions = document.querySelectorAll('ytmusic-menu-service-item-renderer');
                // We use a more strict filter to avoid "Play next"
                const addToQueue = Array.from(menuOptions).find(el => {
                    const text = el.textContent.trim().toLowerCase();
                    return text === actionLabel;
                });

                if (addToQueue) {
                    addToQueue.click();
                    console.log("Success: Added to the end of the queue!");
                } else {
                    console.error("Found the menu, but couldn't find the exact 'Add to queue' button.");
                }
            }, 400);
            return true;
        }
        return false;
    }

    // Attempt to run, and if search results aren't ready, try again in 1 second
    if (!tryAddToQueue()) {
        setTimeout(tryAddToQueue, 1500);
    }
}

    setInterval(poll, 1500);
})();