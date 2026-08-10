/// <reference types="vite/client" />
/// <reference types="vite-plugin-svgr/client" />

declare global {
  namespace JSX {
    interface Element extends React.JSX.Element {}
    interface ElementClass extends React.JSX.ElementClass {}
    interface ElementAttributesProperty
      extends React.JSX.ElementAttributesProperty {}
    interface ElementChildrenAttribute
      extends React.JSX.ElementChildrenAttribute {}
    interface IntrinsicAttributes extends React.JSX.IntrinsicAttributes {}
    interface IntrinsicClassAttributes<T>
      extends React.JSX.IntrinsicClassAttributes<T> {}
    interface IntrinsicElements extends React.JSX.IntrinsicElements {}
  }
}

interface ImportMetaEnv {
  readonly BACKEND_URL: string;
  readonly ACCESS_TOKEN_EXPIRE_SECONDS: string;
  readonly CI: string;
  readonly LANGFLOW_AUTO_LOGIN: string;
  readonly LANGFLOW_MCP_COMPOSER_ENABLED: string;
}

interface ImportMeta {
  readonly env: ImportMetaEnv;
}

interface Window {
  __LANGFLOW_RUNTIME_CONFIG__?: {
    LANGFLOW_UNAUTHORIZED_REDIRECT_URL?: string;
  };
}

declare module "*.svg" {
  const content: string;
  export default content;
}
