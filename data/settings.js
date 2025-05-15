module.exports = {

/*******************************************************************************
// Flow File and User Directory Settings
//  - flowFile
//  - credentialSecret
//  - flowFilePretty
//  - userDir
//  - nodesDir
******************************************************************************/

    flowFile: 'flows.json',
    flowFilePretty: true,

/*******************************************************************************
// Security
//  - adminAuth
//  - https
//  - httpsRefreshInterval
//  - requireHttps
//  - httpNodeAuth
//  - httpStaticAuth
******************************************************************************/

    // ... (Keep security settings as they are or configure as needed)

/*******************************************************************************
// Server Settings
//  - uiPort
//  - uiHost
//  - apiMaxLength
//  - httpServerOptions
//  - httpAdminRoot
//  - httpAdminMiddleware
//  - httpAdminCookieOptions
//  - httpNodeRoot
//  - httpNodeCors
//  - httpNodeMiddleware
//  - httpStatic
//  - httpStaticRoot
//  - httpStaticCors
******************************************************************************/

    uiPort: process.env.PORT || 1880,
    uiHost: "0.0.0.0", // To accept connections from any host

/*******************************************************************************
// Logging - Set the log level to 'debug' for detailed logs
******************************************************************************/

    logging: {
        console: {
            level: "debug", // Set to debug for detailed logs
            metrics: false,
            audit: false
        }
    },

/*******************************************************************************
// Runtime Settings
//  - lang
//  - runtimeState
//  - diagnostics
//  - logging
//  - contextStorage
//  - exportGlobalContextKeys
//  - externalModules
******************************************************************************/

    diagnostics: {
        enabled: true,
        ui: true,
    },

    runtimeState: {
        enabled: false,
        ui: false,
    },

    // Enable function-global context
    functionGlobalContext: {
        // Any required global context can be added here
    },

/*******************************************************************************
// Editor Settings
******************************************************************************/

    editorTheme: {
        palette: {
            // Optionally, customize the palette for nodes
        },
    },

/*******************************************************************************
// Node Settings
******************************************************************************/

    functionExternalModules: true,
    functionTimeout: 0,
    debugMaxLength: 1000, // Increase the max debug length to see more detailed logs
    mqttReconnectTime: 15000,
    serialReconnectTime: 15000,
    // Other node settings can be configured as needed
}
