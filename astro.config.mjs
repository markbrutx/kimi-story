import { defineConfig } from 'astro/config';

// https://astro.build/config
export default defineConfig({
  site: 'https://markbrutx.github.io',
  base: '/kimi-story',
  output: 'static',
  build: {
    format: 'file',
    assets: 'assets'
  },
  vite: {
    build: {
      cssMinify: true,
      minify: true
    }
  }
});
