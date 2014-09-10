staticPath = 'static_src/';
jsPath = staticPath + 'js/';
sassPath = staticPath + 'sass/';
templatePath = staticPath + 'templates/';
buildPath = 'build/';
buildSass = buildPath + 'sass/';
bowerPath = 'bower_components/';
distPath = 'static/dashboard/';

module.exports = function (grunt) {
    // load all grunt tasks matching the `grunt-*` pattern
    require('load-grunt-tasks')(grunt);

    grunt.initConfig({
        ngtemplates: {
            app: {
                cwd: templatePath,
                src: "**/*.html",
                dest: buildPath + "templates.dist.js",
                options: {
                    module: "Templates",
                    standalone: true,
                    concat: "js",
                    htmlmin: {
                      collapseBooleanAttributes:      true,
                      collapseWhitespace:             true,
                      removeAttributeQuotes:          true,
                      removeComments:                 true,
                      removeEmptyAttributes:          true,
                      removeRedundantAttributes:      true,
                      removeScriptTypeAttributes:     true,
                      removeStyleLinkTypeAttributes:  true
                    }
                }
            }
        },

        concat: {
            js: {
                src: [
                    bowerPath + "angular/angular.js",
                    bowerPath + "angular-route/angular-route.js",
                    bowerPath + "angular-cookies/angular-cookies.js",
                    bowerPath + "lodash/dist/lodash.js",
                    jsPath + "DashboardApp.js",
                    jsPath + "controllers/*.js",
                    jsPath + "services/*.js",
                    jsPath + "directives/*.js",
                    '<%= ngtemplates.app.dest %>'
                ],
                dest: distPath + 'app.dist.js'
            }
        },

        copy: {
            sass: {
                files: [
                    {expand: true, cwd: bowerPath + 'bourbon/dist/', src:['**'], dest: buildPath + 'sass/bourbon/'},
                    {expand: true, cwd: bowerPath + 'neat/app/assets/stylesheets/', src:['**'], dest: buildPath + 'sass/neat/'},
                    {expand: true, cwd: sassPath, src:['**'], dest: buildPath + 'sass/'}
                ]
            }
        },

        sass: {
            dashboard: {
                files: {
                    'static/dashboard/dashboard.dist.css': 'build/sass/dashboard.scss'
                }
            }
        },

        watch: {
            app: {
                files: ["static_src/**/*"],
                tasks: ["_default"]
            }
        }
    });
    grunt.registerTask('default', ['_default', 'watch:app']);
    grunt.registerTask('_default', ['concat', 'ngtemplates', 'copy', 'sass']);
}
