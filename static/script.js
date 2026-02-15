function add(e,title,artist,id,action) {
    const btn = e.currentTarget;
    console.log(title + " " + artist + " " + action + " " + id)
    
    btn.classList.add('active-click');

    setTimeout(() => {
        btn.classList.remove('active-click');
    }, 500);


    fetch("http://localhost:3000/command", {
        method: "POST",
        body: JSON.stringify({
            "videoId": id, 
            "title": title,
            "artist": artist,
            "action": action
        }),
        headers: {
            "Content-type": "application/json; charset=UTF-8"
        }
    });
}

function apiCall() {
    const container = document.getElementById("container")
    var searchInput = document.getElementById("searchYTM");

    searchInput.onkeydown = stupidFunction();
    function stupidFunction() {
        var searchData = document.getElementById("searchYTM").value;

        if (searchData.length >= 0 ) {
            while (document.getElementsByClassName('autoComplete')[0]) {
                document.getElementsByClassName('autoComplete')[0].remove();
            }
        }

        var request = new XMLHttpRequest();
        request.open('GET', '/suggestion/' + searchData, true);
        request.onload = function () {
            var data = JSON.parse(this.response);

            var wrapper = document.createElement('div');
            wrapper.className = "autoComplete";
            container.appendChild(wrapper);
            if (request.status >= 200 && request.status < 400) {
                data.forEach(res => {

                    const searchResultsContainer = document.createElement('div');
                    searchResultsContainer.setAttribute('class', 'row');

                    const h1 = document.createElement('a');
                    h1.textContent = res;
                    h1.href = "/search/" + res
                    wrapper.appendChild(searchResultsContainer);
                    searchResultsContainer.appendChild(h1);
                });
            } else {
                console.log('error');
            }
        };
        request.send();
    }
}

document.addEventListener('DOMContentLoaded', function() {
// Get the input field
var input = document.getElementById("searchYTM");

// Execute a function when the user presses a key on the keyboard
input.addEventListener("keypress", function(event) {
    console.log("test");
  // If the user presses the "Enter" key on the keyboard
  if (event.key === "Enter") {
    // Cancel the default action, if needed
    event.preventDefault();
    // Trigger the button element with a click
    window.location.href = "/search/" + input.value;
  }
});
});