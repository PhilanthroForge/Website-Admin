
# Unsplash Routes
@app.route('/admin/api/unsplash/search', methods=['GET'])
@login_required
def search_unsplash():
    query = request.args.get('query', '')
    page = request.args.get('page', 1)
    if not query:
        return jsonify({'results': []})
    
    from unsplash import search_photos
    data = search_photos(query, page)
    return jsonify(data)

@app.route('/admin/api/unsplash/download', methods=['POST'])
@login_required
def download_unsplash():
    data = request.json
    download_location = data.get('download_location')
    photo_id = data.get('id')
    
    if not download_location:
         return jsonify({'error': 'Missing download location'}), 400
         
    from unsplash import download_photo
    local_path = download_photo(download_location, photo_id)
    
    if local_path:
        return jsonify({'success': True, 'path': local_path})
    else:
        return jsonify({'error': 'Download failed'}), 500
