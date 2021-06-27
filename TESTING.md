# Contents

   * [Testing User Stories](#Testing-User-Stories)
   * [Validators](#Validators)
      * [HTML Validators](#HMTL-Validators)
         * [HTML Pages](#HTML-Pages)
         * [Data Sensitive HTML Pages](#Data-Sensitive-HTML-Pages)
   * [Testing Features](#Testing-Features)
        * [Navigation](#Navigation)
        
        * [Social Media Links](#Social-Media-Links)
        * [Buttons and Solutions Functions](#Buttons-and-Solutions-Functions)
        * [Alerts](#Alerts)
        
        * [Contact Form](#Contact-Form)
        * [404 Page](#404-Page)
   * [Manual Testing of Route Handlers](#Manual-Testing-of-Route-Handlers)
   * [Site Responsiveness](#Site-Responsiveness)
   * [User Testing](#User-Testing)
   * [Known Bugs and Issues](#Known-Bugs-and-Issues)
   * [Further Testing](#Further-Testing) 

## Validators
### HTML 
#### HTML Pages
#### Data Sensitive HTML Pages

Because some of the pages of the site contain an Object ID in the url the validation results of these pages are listed below instead of using photos.

* **Edit Article Page** &#40; `edit_article.html` &#41;: 0 Errors & 0 Warnings Found
* **Edit Topic Page** &#40; `edit_topic.html` &#41;: 0 Errors & 0 Warnings Found
* **Edit Further Reading Page** &#40; `edit_further_reading.html` &#41;: 0 Errors & 0 Warnings Found

## Manual Testing of Route Handlers
* In order to ensure each route handler performed correctly with regards to security features and defensive programming the following steps were taken to test each relevent route handler:
   1. Sign into MotherFolklore as Admin.
   2. Navigate to the relevant pages that are user/Admin specific and copy the relevant url.
   3. Sign Out as Admin.
   4. Sign in as a standard user.
   5. Paste the relevant url into the google search bar.
   6. Check to see if the page redirects as anticipated. 
      * If the page redirects this confirms that the route handler is functioning as expected and no content from this page can be altered/deleted by anyone other than the content's owner or the site Admin.
      * If the page does not redirect as expected then the route handler has failed to protect the site's content and needs to be fixed. 

### Edit Article Route Handler
* The above steps were implemented to test the edit article route handler. As indicated by the image below, this route handler was functioning as expected at the time of submission by redirecting the user to the articles page and subsequently passed this test. 

* <img src="assets/documentation/doc-images/editarticleroutehandler.png" width="450" height="250" alt="test-edit-article">

### Add Topic Route Handler
* The above steps were implemented to test the add topic route handler. As indicated by the image below, this route handler was functioning as expected at the time of submission by redirecting the user to the topics page and subsequently passed this test. 

* <img src="assets/documentation/doc-images/add-topic-route-handler.png" width="350" height="150" alt="test-add-topic">

### Edit Topic Route Handler
* The above steps were implemented to test the edit topic route handler. As indicated by the image below, this route handler was functioning as expected at the time of submission by redirecting the user to the topics page and subsequently passed this test. 

* <img src="assets/documentation/doc-images/edit-topic-route-handler.png" width="350" height="150" alt="test-edit-topic">

### Add Further Reading Route Handler
* The above steps were implemented to test the add further reading route handler. As indicated by the image below, this route handler was functioning as expected at the time of submission by redirecting the user to the topics page and subsequently passed this test. 

* <img src="assets/documentation/doc-images/add-fr-route-handler.png" width="350" height="150" alt="test-add-further-reading">

### Edit Further Reading Route Handler
* The above steps were implemented to test the edit further reading route handler. As indicated by the image below, this route handler was functioning as expected at the time of submission by redirecting the user to the topics page and subsequently passed this test. 

* <img src="assets/documentation/doc-images/edit-fr-route-handler.png" width="350" height="150" alt="test-edit-further-reading">

* All delete functions do not display id specific urls at the time of deletion so similar tests could not be performed on these functions. However similar defensive programming has been implemented so as to prevent any malicious deletion of content and only allow content to be deleted by the the content's owner or the site admin.

## Known Bugs and Issues
* One known bug was the failure of the parallax container to render on the profile page. The initial file path was as follows on all pages that used these images:
 ```
 <div class="parallax-container login">
 <div class="parallax"> <img src="static/images/banshee3.jpg">
 </div>
 </div>
 ```
In order to trouble shoot the issue the following code was used to try and rectify the problem:
```
<div class="parallax-container">
		<div class="parallax"><img src="{{ url_for('static', filename='images/banshee3.jpg') }}"></div>
	  </div>
```
This code effectively resolved the issue without any problems. The issue was raised with the project's mentor but an explanation could not be found. For the sake of consistency all parallax containers now use the above file path to avoid any unforeseen or inexplicable issues. 

* Another troublesome bug was found on the topics page. Topics created on the site instead of the database failed to push articles into the database list array as can be seen in the images below:

<img src="assets/documentation/doc-images/topicsbug1.png" width="450" height="250" alt="topicsbug1">

After much consultation with tutor support it was discovered that Topics created on the site had failed to pass an empty string value into the MongoDB article list array as can be seen in the image below:

<img src="assets/documentation/doc-images/topicsbug2.png" width="450" height="250" alt="topicsbug2">

After this discovery and a great deal of trouble shooting the following code was added into the add_topic route handler to rectify the issue and ensure that the article list array was initialized with an empty string value: 
```
"article_list": [""]
```