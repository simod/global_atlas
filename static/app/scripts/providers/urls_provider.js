'use strict';

/*
* Provides the backend api communication connections
*/

(function(){
  goog.provide('atlas_url_provider');

  var module = angular.module('atlas_url_provider', []);

  module.provider('UrlsProvider', function(){

    this.$get = function(ApiUrls){

      return {
        format_url: ApiUrls.urls.formats.list_endpoint,
        size_url: ApiUrls.urls.sizes.list_endpoint,
        requester_url: ApiUrls.urls.requesters.list_endpoint,
        country_url: ApiUrls.urls.countries.list_endpoint,
        map_url: ApiUrls.urls.maps.list_endpoint,        
        request_url: ApiUrls.urls.requests.list_endpoint
      }
    }
  });
})();