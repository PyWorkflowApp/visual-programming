/**
 * Add node to server-side workflow
 * @param {CustomNodeModel} node - JS node to add
 * @returns {Promise<Object>} - server response
 */
export async function addNode(node) {
    const payload = {...node.options, options: node.config};
    const resp = await fetch("/node/", {
        method: "POST",
        body: JSON.stringify(payload)
    });
    const json = await resp.json();
    if (resp.ok) {
        console.log(json);
        return json;
    } else {
        console.log("Failed to create node on back end.")
        return Promise.resolve(json);
    }
}


/**
 * Delete node from server-side workflow
 * @param {CustomNodeModel} node - JS node to remove
 * @returns {Promise<Object>} - server response
 */
export async function deleteNode(node) {
    const id = node.options.id;
    const resp = await fetch(`/node/${id}`, {
        method: "DELETE"
    });
    const json = await resp.json();
    if (resp.ok) {
        console.log(json);
        return json
    } else {
        console.log("Failed to delete node on back end.")
        return Promise.reject(json);
    }
}


/**
 * Update configuration of node in server-side workflow
 * @param {CustomNodeModel} node - JS node to remove
 * @param {Object} config - configuration from options form
 * @returns {Promise<Object>} - server response (serialized node)
 */
export async function updateNode(node, config) {
    node.config = config;
    const payload = {...node.options, options: node.config};
    const resp = await fetch(`/node/${node.options.id}`, {
        method: "POST",
        body: JSON.stringify(payload)
    });
    const json = await resp.json();
    if (!resp.ok) {
        console.log("Failed to update node on back end.");
        return Promise.reject(JSON);
    } else {
        console.log(json);
        return json
    }
}


/**
 * Save front-end workflow and download server response as JSON file
 * @param {Object} diagramData - serialized react-diagrams model
 */
export async function save(diagramData) {
    const payload = JSON.stringify(diagramData);
    const resp = await fetch("/workflow/save", {
        method: "POST",
        headers: {"Content-Type": "application/json"},
        body: payload
    });
    const json = await resp.json();
    if (!resp.ok) {
        return Promise.reject(json);
    } else {
        const dataStr = "data:text/json;charset=utf-8,"
            + encodeURIComponent(JSON.stringify(json));
        const anchor = document.createElement("a")
        anchor.href = dataStr;
        anchor.download = json.filename || "diagram.json";
        anchor.click();
        anchor.remove();
    }
}


/**
 * Get available nodes for node menu
 * @returns {Promise<Object>} - server response (node menu items)
 */
export async function getNodes() {
    const resp = await fetch("/nodes");
    const json = await resp.json();
    return resp.ok ? json : Promise.reject(json);
}


/**
 * Start a new workflow on the server
 * @returns {Promise<Object>} - server response
 */
export async function initWorkflow() {
    const resp = await fetch("/workflow/new");
    const json = await resp.json();
    return resp.ok ? json : Promise.reject(json);
}


/**
 * Uploads JSON workflow file to server
 * @param {FormData} formData - form with key `file` and value of type `File`
 * @returns {Promise<Object>} - server response (full serialized workflow)
 */
export async function uploadWorkflow(formData) {
    const resp = await fetch("/workflow/open", {
        method: "POST",
        body: formData
    });
    const json = await resp.json();
    return resp.ok ? json : Promise.reject(json);
}