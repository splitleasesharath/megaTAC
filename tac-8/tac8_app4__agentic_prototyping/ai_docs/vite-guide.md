ViteConf 2025 · First time in-person · Amsterdam · Oct 09-10 [Register](https://viteconf.amsterdam/?utm_source=vite&utm_content=top_banner)

[Skip to content](https://vite.dev/guide/#VPContent)

On this page

# Getting Started [​](https://vite.dev/guide/\#getting-started)

## Overview [​](https://vite.dev/guide/\#overview)

Vite (French word for "quick", pronounced `/vit/`, like "veet") is a build tool that aims to provide a faster and leaner development experience for modern web projects. It consists of two major parts:

- A dev server that provides [rich feature enhancements](https://vite.dev/guide/features) over [native ES modules](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Guide/Modules), for example extremely fast [Hot Module Replacement (HMR)](https://vite.dev/guide/features#hot-module-replacement).

- A build command that bundles your code with [Rollup](https://rollupjs.org/), pre-configured to output highly optimized static assets for production.


Vite is opinionated and comes with sensible defaults out of the box. Read about what's possible in the [Features Guide](https://vite.dev/guide/features). Support for frameworks or integration with other tools is possible through [Plugins](https://vite.dev/guide/using-plugins). The [Config Section](https://vite.dev/config/) explains how to adapt Vite to your project if needed.

Vite is also highly extensible via its [Plugin API](https://vite.dev/guide/api-plugin) and [JavaScript API](https://vite.dev/guide/api-javascript) with full typing support.

You can learn more about the rationale behind the project in the [Why Vite](https://vite.dev/guide/why) section.

## Browser Support [​](https://vite.dev/guide/\#browser-support)

During development, Vite assumes that a modern browser is used. This means the browser supports most of the latest JavaScript and CSS features. For that reason, Vite sets [`esnext` as the transform target](https://esbuild.github.io/api/#target). This prevents syntax lowering, letting Vite serve modules as close as possible to the original source code. Vite injects some runtime code to make the development server work. These code use features included in [Baseline](https://web-platform-dx.github.io/web-features/) Newly Available at the time of each major release (2025-05-01 for this major).

For production builds, Vite by default targets [Baseline](https://web-platform-dx.github.io/web-features/) Widely Available browsers. These are browsers that were released at least 2.5 years ago. The target can be lowered via configuration. Additionally, legacy browsers can be supported via the official [@vitejs/plugin-legacy](https://github.com/vitejs/vite/tree/main/packages/plugin-legacy). See the [Building for Production](https://vite.dev/guide/build) section for more details.

## Trying Vite Online [​](https://vite.dev/guide/\#trying-vite-online)

You can try Vite online on [StackBlitz](https://vite.new/). It runs the Vite-based build setup directly in the browser, so it is almost identical to the local setup but doesn't require installing anything on your machine. You can navigate to `vite.new/{template}` to select which framework to use.

The supported template presets are:

| JavaScript | TypeScript |
| --- | --- |
| [vanilla](https://vite.new/vanilla) | [vanilla-ts](https://vite.new/vanilla-ts) |
| [vue](https://vite.new/vue) | [vue-ts](https://vite.new/vue-ts) |
| [react](https://vite.new/react) | [react-ts](https://vite.new/react-ts) |
| [preact](https://vite.new/preact) | [preact-ts](https://vite.new/preact-ts) |
| [lit](https://vite.new/lit) | [lit-ts](https://vite.new/lit-ts) |
| [svelte](https://vite.new/svelte) | [svelte-ts](https://vite.new/svelte-ts) |
| [solid](https://vite.new/solid) | [solid-ts](https://vite.new/solid-ts) |
| [qwik](https://vite.new/qwik) | [qwik-ts](https://vite.new/qwik-ts) |

## Scaffolding Your First Vite Project [​](https://vite.dev/guide/\#scaffolding-your-first-vite-project)

npmYarnpnpmBunDeno

bash

```
$ npm create vite@latest
```

bash

```
$ yarn create vite
```

bash

```
$ pnpm create vite
```

bash

```
$ bun create vite
```

bash

```
$ deno init --npm vite
```

Then follow the prompts!

Compatibility Note

Vite requires [Node.js](https://nodejs.org/en/) version 20.19+, 22.12+. However, some templates require a higher Node.js version to work, please upgrade if your package manager warns about it.

Using create vite with command line options

You can also directly specify the project name and the template you want to use via additional command line options. For example, to scaffold a Vite + Vue project, run:

npmYarnpnpmBunDeno

bash

```
# npm 7+, extra double-dash is needed:
$ npm create vite@latest my-vue-app -- --template vue
```

bash

```
$ yarn create vite my-vue-app --template vue
```

bash

```
$ pnpm create vite my-vue-app --template vue
```

bash

```
$ bun create vite my-vue-app --template vue
```

bash

```
$ deno init --npm vite my-vue-app --template vue
```

See [create-vite](https://github.com/vitejs/vite/tree/main/packages/create-vite) for more details on each supported template: `vanilla`, `vanilla-ts`, `vue`, `vue-ts`, `react`, `react-ts`, `react-swc`, `react-swc-ts`, `preact`, `preact-ts`, `lit`, `lit-ts`, `svelte`, `svelte-ts`, `solid`, `solid-ts`, `qwik`, `qwik-ts`.

You can use `.` for the project name to scaffold in the current directory.

## Community Templates [​](https://vite.dev/guide/\#community-templates)

create-vite is a tool to quickly start a project from a basic template for popular frameworks. Check out Awesome Vite for [community maintained templates](https://github.com/vitejs/awesome-vite#templates) that include other tools or target different frameworks.

For a template at `https://github.com/user/project`, you can try it out online using `https://github.stackblitz.com/user/project` (adding `.stackblitz` after `github` to the URL of the project).

You can also use a tool like [degit](https://github.com/Rich-Harris/degit) to scaffold your project with one of the templates. Assuming the project is on GitHub and uses `main` as the default branch, you can create a local copy using:

bash

```
npx degit user/project#main my-project
cd my-project

npm install
npm run dev
```

## Manual Installation [​](https://vite.dev/guide/\#manual-installation)

In your project, you can install the `vite` CLI using:

npmYarnpnpmBunDeno

bash

```
$ npm install -D vite
```

bash

```
$ yarn add -D vite
```

bash

```
$ pnpm add -D vite
```

bash

```
$ bun add -D vite
```

bash

```
$ deno add -D npm:vite
```

And create an `index.html` file like this:

html

```
<p>Hello Vite!</p>
```

Then run the appropriate CLI command in your terminal:

npmYarnpnpmBunDeno

bash

```
$ npx vite
```

bash

```
$ yarn vite
```

bash

```
$ pnpm vite
```

bash

```
$ bunx vite
```

bash

```
$ deno run -A npm:vite
```

The `index.html` will be served on `http://localhost:5173`.

## `index.html` and Project Root [​](https://vite.dev/guide/\#index-html-and-project-root)

One thing you may have noticed is that in a Vite project, `index.html` is front-and-central instead of being tucked away inside `public`. This is intentional: during development Vite is a server, and `index.html` is the entry point to your application.

Vite treats `index.html` as source code and part of the module graph. It resolves `<script type="module" src="...">` that references your JavaScript source code. Even inline `<script type="module">` and CSS referenced via `<link href>` also enjoy Vite-specific features. In addition, URLs inside `index.html` are automatically rebased so there's no need for special `%PUBLIC_URL%` placeholders.

Similar to static http servers, Vite has the concept of a "root directory" which your files are served from. You will see it referenced as `<root>` throughout the rest of the docs. Absolute URLs in your source code will be resolved using the project root as base, so you can write code as if you are working with a normal static file server (except way more powerful!). Vite is also capable of handling dependencies that resolve to out-of-root file system locations, which makes it usable even in a monorepo-based setup.

Vite also supports [multi-page apps](https://vite.dev/guide/build#multi-page-app) with multiple `.html` entry points.

#### Specifying Alternative Root [​](https://vite.dev/guide/\#specifying-alternative-root)

Running `vite` starts the dev server using the current working directory as root. You can specify an alternative root with `vite serve some/sub/dir`. Note that Vite will also resolve [its config file (i.e. `vite.config.js`)](https://vite.dev/config/#configuring-vite) inside the project root, so you'll need to move it if the root is changed.

## Command Line Interface [​](https://vite.dev/guide/\#command-line-interface)

In a project where Vite is installed, you can use the `vite` binary in your npm scripts, or run it directly with `npx vite`. Here are the default npm scripts in a scaffolded Vite project:

package.json

json

```
{
  "scripts": {
    "dev": "vite", // start dev server, aliases: `vite dev`, `vite serve`
    "build": "vite build", // build for production
    "preview": "vite preview" // locally preview production build
  }
}
```

You can specify additional CLI options like `--port` or `--open`. For a full list of CLI options, run `npx vite --help` in your project.

Learn more about the [Command Line Interface](https://vite.dev/guide/cli)

## Using Unreleased Commits [​](https://vite.dev/guide/\#using-unreleased-commits)

If you can't wait for a new release to test the latest features, you can install a specific commit of Vite with [https://pkg.pr.new](https://pkg.pr.new/):

npmYarnpnpmBun

bash

```
$ npm install -D https://pkg.pr.new/vite@SHA
```

bash

```
$ yarn add -D https://pkg.pr.new/vite@SHA
```

bash

```
$ pnpm add -D https://pkg.pr.new/vite@SHA
```

bash

```
$ bun add -D https://pkg.pr.new/vite@SHA
```

Replace `SHA` with any of [Vite's commit SHAs](https://github.com/vitejs/vite/commits/main/). Note that only commits within the last month will work, as older commit releases are purged.

Alternatively, you can also clone the [vite repo](https://github.com/vitejs/vite) to your local machine and then build and link it yourself ( [pnpm](https://pnpm.io/) is required):

bash

```
git clone https://github.com/vitejs/vite.git
cd vite
pnpm install
cd packages/vite
pnpm run build
pnpm link --global # use your preferred package manager for this step
```

Then go to your Vite based project and run `pnpm link --global vite` (or the package manager that you used to link `vite` globally). Now restart the development server to ride on the bleeding edge!

Dependencies using Vite

To replace the Vite version used by dependencies transitively, you should use [npm overrides](https://docs.npmjs.com/cli/v11/configuring-npm/package-json#overrides) or [pnpm overrides](https://pnpm.io/9.x/package_json#pnpmoverrides).

## Community [​](https://vite.dev/guide/\#community)

If you have questions or need help, reach out to the community at [Discord](https://chat.vite.dev/) and [GitHub Discussions](https://github.com/vitejs/vite/discussions).