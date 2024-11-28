let state = {};

// Wait until the document is fully loaded
document.addEventListener('DOMContentLoaded', function() {
    waitForPywebview().then(() => {
        pywebview.api.init_frontend().then(initialState => {
            state = initialState;
        });
    }).catch((e) => {
        console.error(e);
    });
});

function waitForPywebview() {
    return new Promise((resolve, reject) => {
        let retries = 10;
        let interval = setInterval(() => {
            if (window.pywebview) {
                clearInterval(interval);
                resolve();
            } else if (retries <= 0) {
                clearInterval(interval);
                reject();
                document.body.style.backgroundColor = "#fd5555";
                document.body.innerHTML = "<h1>Couldn't not establish Pype!</h1>"
            } else {
                console.log("Trying to create Pype!");
                retries--;
            }
        }, 100);
    });
}

// Update specific element's inner HTML
function updateElement(elementId, value) {
    const element = document.getElementById(elementId);
    if (element) {
        element.innerHTML = value;
    }
}

// Set state from UI interaction
function set_state(key, value) {
    pywebview.api.set_state(key, value);
    state[key] = value;
}
