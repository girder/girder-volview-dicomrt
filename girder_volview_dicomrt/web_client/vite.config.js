import { resolve } from 'path';

import { defineConfig } from 'vite';

// The Girder web client provides the global "girder" object; nothing from
// @girder/core is bundled.
export default defineConfig({
  build: {
    sourcemap: !process.env.SKIP_SOURCE_MAPS,
    lib: {
      entry: resolve(__dirname, 'main.js'),
      name: 'GirderPluginVolviewDicomRT',
      fileName: 'girder-plugin-volview-dicomrt',
    },
  },
});
