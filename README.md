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
app.set_state("count", 0)
```

**JavaScript:**  
```javascript
onclick="set_state('count', (state['count'] || 0) + 1)"
```

---

## Binds

**Description:**  
Binds a state to an element via its `key` attribute and specifies which attribute should be updated upon a state change.

**Example:**  
```python
app.bind('count', 'count', HTMLAttributes.INNERHTML)
```

---

## Hooks

**Description:**  
Attaches a function to a specific state change. When the state updates, the hooked function is called.

**Example:**  
```python
app.hook('count', changed_count)
```

---

## Prefabs

### Creation

**Description:**  
Users can create prefabs that can be instantiated or destroyed by the app. Attributes are passed as Python dictionaries.

**Example (HTML):**  
```html
<prefab id="prefab-number">
    <div class="number" style="color: $color; border-color: $color;">$count</div>
</prefab>
```

---

### Instantiate

**Description:**  
Instantiates a prefab with a unique key under a specified parent element, passing attributes to customize its content.

**Example:**  
```python
app.instantiate("prefab-number", f"number-{count}", "prefab-parent", {"count": count, "color": random_color})
```

---

### Destroy

**Description:**  
Destroys a prefab with the specified ID and key. During destruction, the prefab enters its destruction phase and receives the `.destroyed` class for exit animations.

**Example:**  
```python
app.destroy("prefab-number", f"number-{prevCount}")
```
