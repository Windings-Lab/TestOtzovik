import requests


def share_on_linkedin(access_token, linkedin_id, course_name='Course_name'):
    url = 'https://api.linkedin.com/v2/ugcPosts'
    headers = {
        'Authorization': f'Bearer {access_token}',
        'Content-Type': 'application/json',
        'X-Restli-Protocol-Version': '2.0.0'
    }

    data = {
        "author": f"urn:li:person:{linkedin_id}",
        "lifecycleState": "PUBLISHED",
        "specificContent": {
            "com.linkedin.ugc.ShareContent": {
                "shareCommentary": {
                    "text": f"I left the review about the {course_name} on the Otzovik.ua and very glad with a service!!!"
                },
                "shareMediaCategory": "ARTICLE",
                "media": [
                    {
                        "status": "READY",
                        "description": {
                            "text": "Otzovik official site - your way to be clear with yourself and world around!"
                        },
                        "originalUrl": "http://127.0.0.1:8000/home/",
                        "title": {
                            "text": "Otzovik official page"
                        }
                    }
                ]
            }
        },
        "visibility": {
            "com.linkedin.ugc.MemberNetworkVisibility": "PUBLIC"
        }
    }

    requests.post(url=url, json=data, headers=headers)

