# Pype

![logo](https://github.com/kokasmark/pype/blob/main/banner.png?raw=true)

**Fast** and **Simple** GUI framework for Python

Render **Python** computed values and interact them via **HTML** in a webview application

Good for fast visualization or **lightweight applications**

# Documentation

## Project creation

```bash
py plumber.py new project-name
```

## State Management

### Set State
**Python:**  
```python
app.set_state("state-key", 0)
```

**JavaScript:**  
```javascript
onclick="set_state('state-key', (state['state-key'] || 0) + 1)"
```

---

## Binds

**Description:**  
Binds a state to an element via its `key` attribute and specifies which attribute should be updated upon a state change.

**Example:**  
```python
app.bind('state-key', 'element-key', HTMLAttributes.INNERHTML)
```

---

## Hooks

**Description:**  
Attaches a function to a specific state change. When the state updates, the hooked function is called.

**Example:**  
```python
app.hook('state-key', hooked_function)
```

---

## Prefabs

### Creation

**Description:**  
Users can create prefabs that can be instantiated or destroyed by the app. Attributes are passed as Python dictionaries.

**Example (HTML):**  
```html
<prefab id="prefab-name">
    <div class="number" style="color: $attribute-name-2; border-color: $attribute-name-2;">$attribute-name</div>
</prefab>
```

---

### Instantiate

**Description:**  
Instantiates a prefab with a unique key under a specified parent element, passing attributes to customize its content.

**Example:**  
```python
app.instantiate("prefab-name", f"key-prefix-{count}", "prefab-parent-id", {"attribute1": 'something', "attribute2": 0})
```

---

### Destroy

**Description:**  
Destroys a prefab with the specified ID and key. During destruction, the prefab enters its destruction phase and receives the `.destroyed` class for exit animations.

**Example:**  
```python
app.destroy("prefab-name", f"key-prefix-{prevCount}")
```

### Observer

**Description:**  
Observers a state array that contains attributes for prefabs, upon its change automatically instantiates or destroys prefabs.

**Example:**  
```python
app.observe('state-key','prefab-id','key-prefix','prefab-parent-id')
```
