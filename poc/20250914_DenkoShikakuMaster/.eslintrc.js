module.exports = {
  root: true,
  env: {
    es2021: true,
    node: true,
    jest: true,
    'react-native/react-native': true,
  },
  extends: [
    'eslint:recommended',
    'plugin:react/recommended',
    'plugin:react-hooks/recommended',
    'plugin:@typescript-eslint/recommended',
    'plugin:prettier/recommended',
    '@react-native-community',
    'airbnb',
    'airbnb-typescript',
  ],
  parser: '@typescript-eslint/parser',
  parserOptions: {
    ecmaFeatures: {
      jsx: true,
    },
    ecmaVersion: 'latest',
    sourceType: 'module',
    project: './tsconfig.json',
  },
  plugins: ['react', 'react-native', 'react-hooks', '@typescript-eslint', 'prettier'],
  rules: {
    // Prettierとの競合を避ける
    'prettier/prettier': ['error', { endOfLine: 'auto' }],

    // React 17以降は不要なためOFF
    'react/react-in-jsx-scope': 'off',

    // .tsxファイルでJSXを許可
    'react/jsx-filename-extension': [
      'error',
      { extensions: ['.ts', '.tsx'] },
    ],

    // TypeScriptでのimport/export関連
    'import/prefer-default-export': 'off',
    'import/extensions': [
      'error',
      'ignorePackages',
      {
        ts: 'never',
        tsx: 'never',
      },
    ],

    // 関数の戻り値の型を明示的に要求しない（型推論に任せる）
    '@typescript-eslint/explicit-module-boundary-types': 'off',
    '@typescript-eslint/explicit-function-return-type': 'off',

    // 未使用変数は警告に留める
    '@typescript-eslint/no-unused-vars': 'warn',

    // コンポーネント定義をアロー関数に統一
    'react/function-component-definition': [
      'error',
      {
        namedComponents: 'arrow-function',
        unnamedComponents: 'arrow-function',
      },
    ],

    // stateの直接変更を許可（Redux Toolkitなどでの使用を想定）
    'no-param-reassign': ['error', { props: false }],

    // React Native固有のルール
    'react-native/no-unused-styles': 'warn',
    'react-native/split-platform-components': 'off',
    'react-native/no-inline-styles': 'warn',
    'react-native/no-color-literals': 'warn',
    'react-native/no-raw-text': 'error',
  },
  settings: {
    react: {
      version: 'detect',
    },
    'import/resolver': {
      typescript: {},
    },
  },
  ignorePatterns: [
    'node_modules/',
    'build/',
    'dist/',
    'coverage/',
    '*.js', // プロジェクトルートの設定ファイル（babel, metro, jestなど）を無視
  ],
};
