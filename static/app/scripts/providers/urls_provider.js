'use strict';

/*
* Provides the backend api communication connections
*/

(function(){
  goog.provide('atlas_url_provider');

  var module = angular.module('atlas_url_provider', []);

  module.provider('UrlsProvider', function(){

    this.$get = ['$http', 'ApiUrls', function($http, ApiUrls){

      return {
        format_url: ApiUrls.urls.formats.list_endpoint,
        size_url: ApiUrls.urls.sizes.list_endpoint,
        requester_url: ApiUrls.urls.requesters.list_endpoint,
        request_post: function(data){
          $http.post(ApiUrls.urls.requests.list_endpoint, data)
            .success(function(){
              alert('Your request is correctly registered!');
            })
            .error(function(){
              alert('error');
            });
        }
      }
      
    }]
  });
})();