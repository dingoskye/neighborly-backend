import urllib.request
import json
import urllib.error

BASE_URL = "http://127.0.0.1:8001"

def make_request(url, method="GET", data=None):
    req = urllib.request.Request(url, method=method)
    req.add_header('Content-Type', 'application/json')
    
    if data:
        json_data = json.dumps(data).encode('utf-8')
        req.data = json_data

    try:
        with urllib.request.urlopen(req) as response:
            status_code = response.getcode()
            response_body = response.read().decode('utf-8')
            try:
                json_response = json.loads(response_body)
            except:
                json_response = response_body
            return status_code, json_response
    except urllib.error.HTTPError as e:
        return e.code, e.read().decode('utf-8')
    except Exception as e:
        return 500, str(e)

def print_result(name, status_code, response):
    status = "SUCCESS" if status_code in [200, 201] else "FAILED"
    print(f"{name}: {status} ({status_code})")
    if status == "FAILED":
        print(response)
    else:
        print(json.dumps(response, indent=2))
    print("-" * 20)

def verify():
    print("Starting Verification...")
    
    # 1. Create a Post
    print("1. Create Post")
    post_data = {
        "title": "Test Post",
        "subtitle": "Checking the backend",
        "content": "This is a test post created via verification script.",
        "image": "https://example.com/image.jpg",
        "authorId": "user-1"
    }
    code, resp = make_request(f"{BASE_URL}/posts", "POST", post_data)
    print_result("Create Post", code, resp)
    if code not in [200, 201]:
        return
    post_id = resp["id"]

    # 2. Get Post
    print(f"2. Get Post {post_id}")
    code, resp = make_request(f"{BASE_URL}/posts/{post_id}", "GET")
    print_result("Get Post", code, resp)

    # 3. Like Post
    print(f"3. Like Post {post_id}")
    code, resp = make_request(f"{BASE_URL}/posts/{post_id}/like", "POST")
    print_result("Like Post", code, resp)

    # 4. Create Comment
    print(f"4. Create Comment on {post_id}")
    comment_data = {
        "userId": "user-1",
        "content": "Nice post!"
    }
    code, resp = make_request(f"{BASE_URL}/posts/{post_id}/comments", "POST", comment_data)
    print_result("Create Comment", code, resp)

    # 5. Create Event
    print("5. Create Event")
    event_data = {
        "title": "Test Event",
        "description": "A fun test event",
        "image": "https://example.com/event.jpg",
        "date": "2024-02-01",
        "time": "18:00",
        "locationName": "Test Park",
        "locationAddress": "123 Test St",
        "lat": 60.0,
        "lng": 25.0,
        "organizerId": "user-1",
        "category": "Tech"
    }
    code, resp = make_request(f"{BASE_URL}/events", "POST", event_data)
    print_result("Create Event", code, resp)
    if code not in [200, 201]:
        return
    event_id = resp["id"]

    # 6. Join Event
    print(f"6. Join Event {event_id}")
    code, resp = make_request(f"{BASE_URL}/events/{event_id}/join", "POST")
    print_result("Join Event", code, resp)
    
    # 7. Update Profile
    print("7. Update Profile")
    profile_data = {
        "bio": "Updated bio via verification!"
    }
    code, resp = make_request(f"{BASE_URL}/profile", "PUT", profile_data)
    print_result("Update Profile", code, resp)

if __name__ == "__main__":
    verify()
