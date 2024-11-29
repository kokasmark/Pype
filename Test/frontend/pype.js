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
                error("Couldn't establish Pype!")
                clearInterval(interval);
                reject();
            } else {
                console.log("Trying to create Pype!");
                retries--;
            }
        }, 100);
    });
}

// Update specific element's inner HTML
function updateElement(elementId, attribute, value) {
    const element = document.getElementById(elementId);

    if (element) {
        if (attribute === "innerHTML") {
            element.innerHTML = value;
        } else {
            element.setAttribute(attribute, value);
        }
    }
}

// Set state from UI interaction
function set_state(key, value) {
    pywebview.api.set_state(key, value);
    state[key] = value;
}

//Instantiates a prefab defined in the html
function instantiate(prefab_id, key, parent_id, attr) {
    const prefab = document.querySelector(`prefab#${prefab_id}`);
    const parent = document.getElementById(parent_id);
    
    if (!prefab) {
        error(`Prefab with id '${prefab_id}' not found.`, true);
        return;
    }
    
    if (!parent) {
        error(`Parent with id '${parent_id}' not found.`, true);
        return;
    }

    let prefabContent = prefab.innerHTML;
    
    attr = JSON.parse(attr);
    attr.forEach((value, index) => {
        const placeholder = new RegExp(`\\$${index}`, 'g');
        prefabContent = prefabContent.replace(placeholder, value);
    });

    const container = document.createElement('div');
    container.setAttribute('data-prefab-id', prefab_id);
    container.setAttribute('data-key', key);

    const contentContainer = document.createElement('div');
    contentContainer.innerHTML = prefabContent;

    container.appendChild(contentContainer);

    parent.appendChild(container);
}

//Destroys a targeted prefab
function destroy(prefab_id, key) {
    const element = document.querySelector(`[data-prefab-id='${prefab_id}'][data-key='${key}']`);

    if (element) {
        element.classList.add('destroyed')
        setTimeout(() => {
            element.remove();
        }, 100);
    } else {
        error(`Prefab with id '${prefab_id}' and key '${key}' not found.`,true);
    }
}

function error(message, fade = false) {
    const errorDiv = document.createElement("div");
    errorDiv.id = "pype-error"; 
    errorDiv.style.position = "fixed";
    errorDiv.style.top = "0";
    errorDiv.style.left = "0";
    errorDiv.style.width = "100%";
    errorDiv.style.height = "100%";
    errorDiv.style.backgroundColor = "#fd5555";
    errorDiv.style.color = "white";
    errorDiv.style.display = "flex";
    errorDiv.style.alignItems = "center";
    errorDiv.style.justifyContent = "center";
    errorDiv.style.fontSize = "2em";
    errorDiv.style.transition = "1s"; 
    errorDiv.style.opacity = "1";

    errorDiv.innerHTML = `<h3>${message}</h3>`;

    document.body.appendChild(errorDiv);

    if (fade) {
        setTimeout(() => {
            errorDiv.style.opacity = "0"; 
            setTimeout(() => {
                document.body.removeChild(errorDiv);
            }, 1000);
        }, 1000);
    }
}

