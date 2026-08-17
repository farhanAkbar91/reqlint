import { defineConfig } from 'cypress';

export default defineConfig({
  e2e: {
    baseUrl: 'http://localhost:3000',
    specPattern: 'tests-e2e/e2e/**/*.spec.ts',
    supportFile: false,
  },
});
