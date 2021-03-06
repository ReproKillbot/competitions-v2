var CODALAB = {}

CODALAB.URLS = []  // Set in base.html
CODALAB.events = riot.observable()

// Private function, shouldn't be directly used
var _upload_ajax = function(endpoint, form_data, progress_update_callback) {
    return $.ajax({
        type: 'PUT',
        url: endpoint,
        data: form_data,
        processData: false,
        contentType: false,
        xhr: function (xhr) {
            var request = new window.XMLHttpRequest();

            // Upload progress
            request.upload.addEventListener("progress", function (event) {
                if (event.lengthComputable) {
                    var percent_complete = event.loaded / event.total;
                    if (progress_update_callback) {
                        progress_update_callback(percent_complete * 100);
                    }
                }
            }, false);
            return request;
        }
    })
}

CODALAB.api = {
    request: function (method, url, data) {
        return $.ajax({
            type: method,
            url: url,
            data: JSON.stringify(data),
            contentType: "application/json",
            dataType: 'json'
        })
    },

    search: function (query) {
        // Todo This should call chahub??
        return CODALAB.api.request('GET', URLS.API + "query/?q=" + query)
    },

    /*---------------------------------------------------------------------
         Competitions
    ---------------------------------------------------------------------*/
    get_competition: function (pk) {
        return CODALAB.api.request('GET', URLS.API + "competitions/" + pk + "/")
    },
    get_competitions: function (query) {
        // To not pass "undefined" in URL...
        query = query || ''
        return CODALAB.api.request('GET', URLS.API + "competitions/" + query)
    },
    create_competition: function (data) {
        return CODALAB.api.request('POST', URLS.API + "competitions/", data)
    },
    get_competition_creation_status: function (key) {
        return CODALAB.api.request('GET', `${URLS.API}competition_status/${key}/`)
    },
    update_competition: function (data, pk) {
        return CODALAB.api.request('PATCH', URLS.API + "competitions/" + pk + "/", data)
    },

    /*---------------------------------------------------------------------
         Submissions
    ---------------------------------------------------------------------*/
    get_submissions: function (query, type) {
        // return CODALAB.api.request('GET', URLS.API + `submissions/?q=${query || ''}&type=${type || ''}`)
        return CODALAB.api.request('GET', URLS.API + `submissions/`)
    },
    delete_submission: function (id) {
        return CODALAB.api.request('DELETE', URLS.API + "submissions/" + id + "/")
    },
    // create_submission: function (form_data, progress_update_callback) {
    //     // NOTE: this function takes a special "form_data" not like the normal
    //     // dictionary other methods take
    //
    //
    //     /*
    //         Set variable CODALAB.IS_SERVER_LOCAL_STORAGE = true or false via context variable
    //
    //         Local storage:
    //             * POST to server
    //
    //         Remote storage:
    //             * POST to server
    //             * Server returns SAS URL
    //             * PUT to SAS URL
    //             * POST to mark upload as done, so un-finished uploads can be pruned later
    //
    //     */
    //     return _upload_ajax(URLS.API + "submissions/", form_data, progress_update_callback)
    // },
    create_submission: function(submission_metadata) {
        return CODALAB.api.request('POST', URLS.API + "submissions/", submission_metadata)
    },

    /*---------------------------------------------------------------------
         Datasets
    ---------------------------------------------------------------------*/
    get_datasets: function (query, type) {
        return CODALAB.api.request('GET', URLS.API + `datasets/?q=${query || ''}&type=${type || ''}`)
    },
    delete_dataset: function (id) {
        return CODALAB.api.request('DELETE', URLS.API + "datasets/" + id + "/")
    },
    /**
     * Creates a dataset
     * @param {object} metadata - name, description, type, data_file, is_public
     * @param {object} data_file - the actual file object to use
     * @param {function} progress_update_callback
     */
    create_dataset: function (metadata, data_file, progress_update_callback) {
        // TODO: CHECK WHAT KIND OF STORAGE WE ARE! ???

        // Pass the requested file name for the SAS url
        metadata.request_sassy_file_name = data_file.name

        // This will be set on successful dataset creation, then used to complete the dataset upload
        var dataset = {}

        return CODALAB.api.request('POST', URLS.API + "datasets/", metadata)
            // We have an upload URL, so upload now..
            .then(function(result) {
                dataset = result
                return $.ajax({
                    type: 'PUT',
                    url: result.sassy_url,
                    data: data_file,
                    processData: false,
                    contentType: false,
                    beforeSend: function(request) {
                        if(STORAGE_TYPE === 'azure') {
                            request.setRequestHeader('x-ms-blob-type', 'BlockBlob')
                            request.setRequestHeader('x-ms-version', '2018-03-28')
                        }
                    },
                    xhr: function (xhr) {
                        var request = new window.XMLHttpRequest();

                        // Upload progress
                        request.upload.addEventListener("progress", function (event) {
                            if (event.lengthComputable) {
                                var percent_complete = event.loaded / event.total;
                                if (progress_update_callback) {
                                    progress_update_callback(percent_complete * 100);
                                }
                            }
                        }, false);
                        return request;
                    }
                })
            })
            // Now we should complete the upload by telling Codalab! (so competition unpacking and such can start)
            .then(function() {
                return CODALAB.api.request('PUT', URLS.API + "datasets/completed/" + dataset.key + "/")
            })
    },
}
