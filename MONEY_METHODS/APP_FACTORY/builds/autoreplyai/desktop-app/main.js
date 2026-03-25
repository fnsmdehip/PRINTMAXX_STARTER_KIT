const { app, BrowserWindow, ipcMain } = require('electron');
const path = require('path');
const Store = require('electron-store');
const store = new Store();

let mainWindow;

function createWindow() {
  mainWindow = new BrowserWindow({
    width: 1200,
    height: 800,
    webPreferences: {
      nodeIntegration: true,
      contextIsolation: false
    }
  });

  mainWindow.loadFile('index.html');
}

app.whenReady().then(() => {
  createWindow();

  app.on('activate', () => {
    if (BrowserWindow.getAllWindows().length === 0) {
      createWindow();
    }
  });
});

app.on('window-all-closed', () => {
  if (process.platform !== 'darwin') {
    app.quit();
  }
});

// Handle website scanning
ipcMain.handle('scan-website', async (event, url) => {
  try {
    // Here we'll add the logic to scan the website and detect the platform
    // For now, we'll return a mock response
    return {
      platform: 'wordpress',
      status: 'success'
    };
  } catch (error) {
    return {
      status: 'error',
      message: error.message
    };
  }
});

// Handle widget installation
ipcMain.handle('install-widget', async (event, { url, platform }) => {
  try {
    // Here we'll add the logic to install the widget based on the platform
    // For now, we'll return a mock success
    return {
      status: 'success',
      message: 'Widget installed successfully'
    };
  } catch (error) {
    return {
      status: 'error',
      message: error.message
    };
  }
}); 