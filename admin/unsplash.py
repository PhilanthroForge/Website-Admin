
"""
Unsplash API Integration Module
"""
import os
import requests
import uuid
from config import Config

UNSPLASH_API_URL = "https://api.unsplash.com"

def search_photos(query, page=1, per_page=12):
    """
    Search photos on Unsplash
    """
    headers = {
        "Authorization": f"Client-ID {Config.UNSPLASH_ACCESS_KEY}",
        "Accept-Version": "v1"
    }
    
    params = {
        "query": query,
        "page": page,
        "per_page": per_page
    }
    
    try:
        url = f"{UNSPLASH_API_URL}/search/photos"
        # print(f"DEBUG: Requesting {url} with query '{query}'")
        response = requests.get(url, headers=headers, params=params)
        
        # Automatic Fallback on Auth Error
        if response.status_code in [401, 403]:
            print(f"DEBUG: Unsplash Auth Error ({response.status_code}). Falling back to MOCK.")
            return get_mock_unsplash_results(query, is_fallback=True)

        if response.status_code != 200:
            print(f"DEBUG: Unsplash Error {response.status_code}: {response.text}")
            return {"error": f"Unsplash API Error: {response.status_code}", "results": []}
        
        response.raise_for_status()
        data = response.json()
        
        # Transform for easier frontend consumption
        results = []
        for photo in data.get('results', []):
            results.append({
                "id": photo['id'],
                "thumb": photo['urls']['thumb'],
                "regular": photo['urls']['regular'],
                "download_location": photo['links']['download_location'],
                "photographer": photo['user']['name'],
                "photographer_link": photo['user']['links']['html'],
                "description": photo['alt_description'] or photo['description'] or "Unsplash Image"
            })
            
        return {
            "total": data['total'],
            "total_pages": data['total_pages'],
            "results": results,
            "is_mock": False
        }
        
    except requests.RequestException as e:
        print(f"Unsplash API Exception: {e}")
        # Fallback on connection error too
        return get_mock_unsplash_results(query, is_fallback=True)

def get_mock_unsplash_results(query, is_fallback=False):
    """Return mock results using Placehold.co"""
    results = []
    topics = ['Nature', 'Office', 'Technology', 'People', 'Meeting', 'Building']
    
    for i, topic in enumerate(topics):
        display_text = f"{topic} ({query or 'Search'})"
        safe_text = display_text.replace(" ", "+")
        colors = ['3b82f6', '10b981', 'f59e0b', 'ef4444', '8b5cf6', 'ec4899']
        bg_color = colors[i % len(colors)]
        
        thumb_url = f"https://placehold.co/400x400/{bg_color}/white?text={safe_text}"
        download_url = f"https://placehold.co/1200x800/{bg_color}/white?text={safe_text}"
        
        results.append({
            "id": f"mock-{i}-{topic}",
            "thumb": thumb_url,
            "regular": download_url,
            "download_location": download_url, 
            "photographer": "System Mock",
            "photographer_link": "#",
            "description": f"Demo Result for {query}"
        })
        
    return {
        "total": len(results),
        "total_pages": 1,
        "results": results,
        "is_mock": True,
        "message": "Invalid API Key - Showing Demo Data" if is_fallback else "Demo Mode"
    }

def download_photo(download_location, photo_id):
    """
    Trigger Unsplash download event and save image locally
    """
    # 0. Check for Mock
    if str(photo_id).startswith('mock-'):
        try:
            img_url = download_location
            img_resp = requests.get(img_url)
            img_resp.raise_for_status()
            
            filename = f"unsplash_mock_{uuid.uuid4().hex[:6]}.jpg"
            save_path = os.path.join(Config.UPLOAD_FOLDER, filename)
            os.makedirs(Config.UPLOAD_FOLDER, exist_ok=True)
            
            with open(save_path, 'wb') as f:
                f.write(img_resp.content)
            
            return f"assets/uploads/{filename}"
        except Exception as e:
            print(f"Mock Download Error: {e}")
            return None

    headers = {
        "Authorization": f"Client-ID {Config.UNSPLASH_ACCESS_KEY}",
        "Accept-Version": "v1"
    }
    
    try:
        # 1. Trigger the download endpoint
        track_resp = requests.get(download_location, headers=headers)
        track_resp.raise_for_status()
        download_url = track_resp.json().get('url')
        
        # 2. Download the actual image
        img_resp = requests.get(download_url)
        img_resp.raise_for_status()
        
        # 3. Save locally
        filename = f"unsplash_{photo_id}_{uuid.uuid4().hex[:6]}.jpg"
        save_path = os.path.join(Config.UPLOAD_FOLDER, filename)
        
        os.makedirs(Config.UPLOAD_FOLDER, exist_ok=True)
        
        with open(save_path, 'wb') as f:
            f.write(img_resp.content)
            
        return f"assets/uploads/{filename}"
        
    except requests.RequestException as e:
        print(f"Download Error: {e}")
        return None
    
    try:
        # 1. Trigger the download endpoint (Required by API terms)
        # This returns the actual URL to download from
        track_resp = requests.get(download_location, headers=headers)
        track_resp.raise_for_status()
        download_url = track_resp.json().get('url')
        
        # 2. Download the actual image
        img_resp = requests.get(download_url)
        img_resp.raise_for_status()
        
        # 3. Save locally
        filename = f"unsplash_{photo_id}_{uuid.uuid4().hex[:6]}.jpg"
        save_path = os.path.join(Config.UPLOAD_FOLDER, filename)
        
        # Ensure directory exists
        os.makedirs(Config.UPLOAD_FOLDER, exist_ok=True)
        
        with open(save_path, 'wb') as f:
            f.write(img_resp.content)
            
        # Return relative path for frontend
        return f"assets/uploads/{filename}"
        
    except requests.RequestException as e:
        print(f"Download Error: {e}")
        return None
