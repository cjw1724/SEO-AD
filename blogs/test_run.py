import os
import sys

sys.path.append(r'd:\SEO AD\blogs')

import main
import tools

# Mock tools
def mock_publish(title: str, content: str) -> str:
    print(f'\n[MOCK] Publishing to Blogger - Title: {title}\n[MOCK] Content length: {len(content)}')
    return f'Successfully published! URL: http://mock-blogger-url.com/post'

def mock_thumbnail(prompt: str) -> str:
    print(f'\n[MOCK] Generating thumbnail for prompt: {prompt}')
    return '<img src="http://mock-thumbnail-url.com/img.jpg" alt="Generated Thumbnail" />'

tools.publish_to_blogger._run = mock_publish
tools.generate_thumbnail_tool._run = mock_thumbnail

# Force it to pick a specific goal to test
main.random.choice = lambda x: x[0] # Pick the finance one

print('Starting mock run...')
try:
    main.run_blog_automation()
except Exception as e:
    import traceback
    traceback.print_exc()
