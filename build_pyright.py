with open('./node_modules/pyright/package.json', 'w') as f:
    content = f.read()
    content = content.replace('"index.js"', '"langserver.index.js"')
    f.write(content)
