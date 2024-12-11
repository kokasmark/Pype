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
function updateElement(elementKey, attribute, value) {
    const elements = document.querySelectorAll(`[key="${elementKey}"]`);

    elements.forEach(element => {
        if (attribute === "innerHTML") {
            element.innerHTML = value;
        } else {
            element.setAttribute(attribute, value);
        }
    });
}

function window_event(event){
    pywebview.api.window_event(event)
}

//Calls a function on the other side
function call(name,attributes=[]){
    pywebview.api.call(name,attributes)
}

//Unloads current page after exit animation it calls load_page_immidiate
function unload(index){
    document.body.classList.add('unloaded');
    setTimeout(() => {
        pywebview.api.load_page_immidiate(index)
    }, 300);
}

// Applies and finalizes state changes calling observers and hooks
function push(keys) {
    pywebview.api.push(keys,state).then(() => {
        keys.forEach(key => {
            pull(key);
        });
    }); 
}

// Set state from UI interaction
function pull(key) {
    pywebview.api.pull(key).then(value => {
        state[key] = value;
        return value;
    });
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

    for (const [name, value] of Object.entries(attr)) { 
        const placeholder = new RegExp(`\\$${name}`, 'g'); 
        prefabContent = prefabContent.replace(placeholder, value); 
    }

    const container = document.createElement('div');
    container.setAttribute('data-prefab-id', prefab_id);
    container.setAttribute('key', key);

    const contentContainer = document.createElement('div');
    contentContainer.innerHTML = prefabContent;

    container.appendChild(contentContainer);

    parent.appendChild(container);
}

//Destroys a targeted prefab
function destroy(prefab_id, key) {
    const element = document.querySelector(`[data-prefab-id='${prefab_id}'][key='${key}']`);

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

