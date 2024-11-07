import requests

def get_posts():
    response = requests.get("https://jsonplaceholder.typicode.com/posts")
    if response.status_code == 200:
        return response.json()
    else:
        return None
    
def main():
    posts = get_posts()
    if posts:
        for post in posts[:5]:
            print(f"Title: {post['title']}\nBody: {post['body']}\n")
    else:
        print("Failed to retrieve posts")

if __name__ == "__main__":
    main()