import glob

GTAG = '''  <!-- Google tag (gtag.js) -->
  <script async src="https://www.googletagmanager.com/gtag/js?id=G-J5YT0HDKHY"></script>
  <script>
    window.dataLayer = window.dataLayer || [];
    function gtag(){dataLayer.push(arguments);}
    gtag('js', new Date());
    gtag('config', 'G-J5YT0HDKHY');
  </script>'''

for path in glob.glob('blockdag-monitor/website/*.html'):
    content = open(path, encoding='utf-8').read()
    if 'G-J5YT0HDKHY' not in content:
        content = content.replace('<head>', '<head>\n' + GTAG, 1)
        open(path, 'w', encoding='utf-8').write(content)
        print('Updated:', path)
    else:
        print('Already has gtag:', path)
