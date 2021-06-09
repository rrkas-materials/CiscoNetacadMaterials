var pageView;
function mediaReady(media) {
  if (pageView) {
    pageView.setMedia(media);
  }
}


window.addEventListener('load', function() {
  permission.check(function(success) {
    if (success) {

      //restrict tabbing to oerlay elements only
      var options = {first: "#breadcrumbs-module"};
      $("#container").tabGuard(options);  

      netacad.configLoader(function() {

        var background = new netacad.models.Background();

        var splashView = new netacad.views.SplashView(background, document.getElementById("splash"), function() {

          var developerTools = new netacad.models.DeveloperTools();

          var contentView = new netacad.views.ContentView(course, document.getElementById("content"));
          var courseMapView = new netacad.views.CourseMapView(course, document.getElementById("map"));
          var courseIndexView = new netacad.views.CourseIndexView(course, document.getElementById("overlay-course-index"));
          var recentPagesView = new netacad.views.RecentPagesView(course, document.getElementById("overlay-recent-pages"));
          var bookmarksView = new netacad.views.BookmarksView(course, document.getElementById("overlay-bookmarks"));
          var backgroundView = new netacad.views.BackgroundView(background, document.body);
          var backgroundsView = new netacad.views.BackgroundsView(background, document.getElementById("overlay-backgrounds"));
          var searchView = new netacad.views.SearchView(course, document.getElementById("overlay-search"));
          var languagesView = new netacad.views.LanguagesView(course, document.getElementById("overlay-languages"));
          var helpView = new netacad.views.HelpView(course, document.getElementById("overlay-help"));
          var developerToolsView = new netacad.views.DeveloperToolsView(developerTools, document.getElementById("overlay-developer"));

          pageView = new netacad.views.PageView(course, document.getElementById("container"));

          $('#menu-course-index').click(function() {
            $('.menu-button.active').removeClass('active');
            $('#menu-course-index').addClass('active');
            courseIndexView.open();

            //restrict tabbing to oerlay elements only
            var options = {first: ".overlay-close-button"};
            $("#overlay-course-index").tabGuard(options);
          
          });

          $('#menu-recent-pages').click(function() {
            $('.menu-button.active').removeClass('active');
            $('#menu-recent-pages').addClass('active');
            recentPagesView.open();

            //restrict tabbing to oerlay elements only
            var options = {first: ".overlay-close-button"};
            $("#overlay-recent-pages").tabGuard(options);
            });

          $('#menu-bookmarks').click(function() {
            $('.menu-button.active').removeClass('active');
            $('#menu-bookmarks').addClass('active');
            bookmarksView.open();

            //restrict tabbing to oerlay elements only
            var options = {first: ".overlay-close-button"};
            $("#overlay-bookmarks").tabGuard(options);
            });

          $('#menu-backgrounds').click(function() {
            $('.menu-button.active').removeClass('active');
            $('#menu-backgrounds').addClass('active');
            backgroundsView.open();

            //restrict tabbing to oerlay elements only
            var options = {first: ".overlay-close-button"};
            $("#overlay-backgrounds").tabGuard(options);
          
          });
          $('#menu-search').click(function() {
            $('.menu-button.active').removeClass('active');
            $('#menu-search').addClass('active');
            searchView.open();

            //restrict tabbing to oerlay elements only
            var options = {first: ".overlay-close-button"};
            $("#overlay-search").tabGuard(options);
          
          });
          if (netacad.config && netacad.config.languages && Object.keys(netacad.config.languages).length) {
            $('#menu-languages').click(function() {
              $('.menu-button.active').removeClass('active');
              $('#menu-languages').addClass('active');
              languagesView.open();

              //restrict tabbing to oerlay elements only
              var options = {first: ".overlay-close-button"};
              $("#overlay-languages").tabGuard(options);
          
            });
          } else {
            $('#menu-languages').hide();
          }
          $('#menu-help').click(function() {
            $('.menu-button.active').removeClass('active');
            $('#menu-help').addClass('active');
            helpView.open();

            //restrict tabbing to oerlay elements only
            var options = {first: ".overlay-close-button"};
            $("#overlay-help").tabGuard(options);
          
          });
          if (netacad.settings.get(netacad.settings.DEVELOPER_KEY)) {
            $('#menu-developer').click(function() {
              $('.menu-button.active').removeClass('active');
              $('#menu-developer').addClass('active');
              developerToolsView.open();

              //restrict tabbing to oerlay elements only
              var options = {first: ".overlay-close-button"};
              $("#overlay-developer").tabGuard(options);
            });
          } else {
            $('#menu-developer').hide();
          }
          var data = netacad.settings.get(netacad.settings.RETURN_KEY);
          if (data) {
            $('#menu-return').click(function() {
              window.location.assign(data);
            });
          } else {
            $('#menu-return').hide();
          }

          // hack for iOS 7 Safari on an iPad,
          // due to a bug where the bottom 20px are cut off in landscape mode
          if (navigator.userAgent.match(/iPad;.*CPU.*OS 7_\d/i)) {
            var menu = document.getElementById("menu");
            function adjust() {
              if (window.innerHeight != document.documentElement.clientHeight) {
                menu.style.setProperty("bottom", "20px");
              } else {
                menu.style.removeProperty("bottom");
              }
            };
            window.addEventListener("orientationchange", adjust);
            window.addEventListener("resize", adjust);
            window.addEventListener("load", adjust);
            adjust();
          }

          course.update();

        });
        $(document.documentElement).removeClass("loading");
      });
    } else {
      var login = document.getElementById('login');
      while (document.body.hasChildNodes()) {
        document.body.removeChild(document.body.lastChild);
      }
      document.body.appendChild(login);
      $(document.documentElement).addClass("denied");
      $(document.documentElement).removeClass("loading");
      if (typeof ga !== 'undefined') {
        ga('set', 'page', '/' + course.li + '/' + course.lang + '/#logincheckfailed');
        ga('set', 'title', 'Login check failed');
        ga('send', 'pageview');
      }
    }
  });
});
