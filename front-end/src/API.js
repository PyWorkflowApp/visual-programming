import { downloadFile } from './utils';

const SERVER = process.env.NODE_ENV === "production" ?
    process.env.REACT_APP_SERVER_URL || "" : "";

/**
 * Sends request to server via fetch API and handles error cases
 * @param {string} endpoint - server endpoint
 * @param {Object} options - options parameter for `fetch` call
 * @returns {Promise<Object>} - server response or error
 */
function fetchWrapper(endpoint, options = {}) {
       return new Promise((resolve, reject) => {
        fetch(`${SERVER}${endpoint}`, options)
            .then(async resp => {
                const data = await resp.json();
                console.log(data);
                if (resp.ok) {
                  return resolve(data);
                } else {
                  return reject(data);
                }
            })
            .catch(err => {
                return reject(err);
            });
    });
}


/**
 * Add node to server-side workflow
 * @param {CustomNodeModel} node - JS node to add
 * @returns {Promise<Object>} - server response
 */
export async function addNode(node) {
    const payload = {...node.options, options: node.config};
    const options = {
        method: "POST",
        body: JSON.stringify(payload)
    };
    return fetchWrapper("/node/", options);
}


/**
 * Delete node from server-side workflow
 * @param {CustomNodeModel} node - JS node to remove
 * @returns {Promise<Object>} - server response
 */
export async function deleteNode(node) {
    const id = node.options.id;
    const options = {
        method: "DELETE"
    };
    const endpoint = node.options.is_global ? "node/global" : "node";
    return fetchWrapper(`/${endpoint}/${id}`, options);
}


/**
 * Update configuration of node in server-side workflow
 * @param {CustomNodeModel} node - JS node to remove
 * @param {Object} config - configuration from options form
 * @param {Object} flowConfig - flow variable configuration options
 * @returns {Promise<Object>} - server response (serialized node)
 */
export async function updateNode(node, config, flowConfig) {
    node.config = config;
    node.options.option_replace = flowConfig;
    const payload = {...node.options, options: node.config};
    const options = {
        method: "POST",
        body: JSON.stringify(payload)
    };
    const endpoint = node.options.is_global ? "node/global" : "node";
    return fetchWrapper(`/${endpoint}/${node.options.id}`, options)
}


/**
 * Save front-end workflow and download server response as JSON file
 * @param {Object} diagramData - serialized react-diagrams model
 */
export async function save(diagramData) {
    const payload = JSON.stringify(diagramData);
    const options = {
        method: "POST",
        body: payload
    };
    fetchWrapper("/workflow/save", options)
        .then(json => {
            downloadFile(JSON.stringify(json), "application/json",
                json.filename || "diagram.json")
        }).catch(err => console.log(err));
}


/**
 * Get available nodes for node menu
 * @returns {Promise<Object>} - server response (node menu items)
 */
export async function getNodes() {
    return fetchWrapper("/workflow/nodes");
}


/**
 * Get global flow variables for workflow
 * @returns {Promise<Object>} - server response (global flow variables)
 */
export async function getGlobalVars() {
    return fetchWrapper("/workflow/globals");
}


/**
 * Start a new workflow on the server
 * @param {DiagramModel} model - Diagram model
 * @returns {Promise<Object>} - server response
 */
export async function initWorkflow(model) {
    const options = {
        method: "POST",
        body: JSON.stringify({
            "id": model.options.id
        })
    };

    return fetchWrapper("/workflow/new", options);
}


/**
 * Uploads JSON workflow file to server
 * @param {FormData} formData - form with key `file` and value of type `File`
 * @returns {Promise<Object>} - server response (full serialized workflow)
 */
export async function uploadWorkflow(formData) {
    const options = {
        method: "POST",
        body: formData
    };
    return fetchWrapper("/workflow/open", options);
}


async function handleEdge(link, method) {
    const sourceId = link.getSourcePort().getNode().options.id;
    const targetId = link.getTargetPort().getNode().options.id;

    let endpoint;

    if (link.getSourcePort().options.in) {
        // If edge goes from IN port -> OUT port, reverse the ports
        endpoint = `/node/edge/${targetId}/${sourceId}`;
    } else {
        // Otherwise, keep source -> target edge
        endpoint = `/node/edge/${sourceId}/${targetId}`;
    }

    return fetchWrapper(endpoint, {method: method});
}


/**
 * Add edge to server-side workflow
 * @param {VPLinkModel} link - JS edge to create
 * @returns {Promise<Object>} - server response
 */
export async function addEdge(link) {
    return handleEdge(link, "POST");
}


/**
 * Delete edge from server-side workflow
 * @param {VPLinkModel} link - JS edge to delete
 * @returns {Promise<Object>} - server response
 */
export async function deleteEdge(link) {
    return handleEdge(link, "DELETE");
}


/**
 * Upload a data file to be stored on the server
 * @param {FormData} formData - FormData with file and nodeId
 * @returns {Promise<Object>} - server response
 */
export async function uploadDataFile(formData) {
    const options = {
        method: "POST",
        body: formData
    };
    return fetchWrapper("/workflow/upload", options);
}


/**
 * Download file by name from server
 * @param {CustomNodeModel} node - node containing file to download
 * @returns {Promise<void>}
 */
export async function downloadDataFile(node) {
    // TODO: make this not a giant security problem
    let contentType;

    const payload = {...node.options, options: node.config};

    // can't use fetchWrapper because it assumes JSON response
    fetch(`${SERVER}/workflow/download`, {
        method: "POST",
        body: JSON.stringify(payload)
    })
        .then(async resp => {
            if (!resp.ok) return Promise.reject(await resp.json());
            contentType = resp.headers.get("content-type");
            let filename = resp.headers.get("Content-Disposition");

            if (contentType.startsWith("text")) {
                resp.text().then(data => {
                    downloadFile(data, contentType, filename);
                })
            }
        }).catch(err => console.log(err));
}


/**
 * Get execution order of nodes in graph
 * @returns {Promise<Object>} - server response (array of node IDs)
 */
export async function executionOrder() {
    return fetchWrapper("/workflow/execute");
}

/**
 * Execute given node on server
 * @param {CustomNodeModel }node - node to execute
 * @returns {Promise<Object>} - server response
 */
export async function execute(node) {
    const id = node.options.id;
    return fetchWrapper(`/node/${id}/execute`);
}

/**
 * Retrieves the data at the state of the specified node
 * @param {string }nodeId - node identifier for an execution state
 * @returns {Promise<Object>} - json respnse with the data at specified state
 */
export async function retrieveData(nodeId) {
  return fetchWrapper(`/node/${nodeId}/retrieve_data`);
}
