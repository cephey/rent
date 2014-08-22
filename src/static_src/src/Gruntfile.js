// Обязательная обёртка
module.exports = function (grunt) {
    // Задачи
    grunt.initConfig({
        // Склеиваем
        concat: {
            main_morris: {
                src: [
                    'main/js/morris/raphael.min.js',
                    'main/js/morris/morris.min.js',
                    'main/js/morris/morris-data.js'
                ],
                dest: 'main/js/_morris_.js'
            },
            pages_float: {
                src: [
                    'pages/js/float/jquery.flot.js',
                    'pages/js/float/jquery.flot.tooltip.min.js',
                    'pages/js/float/jquery.flot.resize.js',
                    'pages/js/float/jquery.flot.pie.js',
                    'pages/js/float/flot-data.js'
                ],
                dest: 'pages/js/_float_.js'
            },
            users: {
                src: ['users/js/scripts/scripts.js'],
                dest: 'users/js/_scripts_.js'
            }
        },
        // Сжимаем js
        uglify: {
            main_morris: {
                files: {
                    '../dest/js/main_morris.min.js': '<%= concat.main_morris.dest %>'
                }
            },
            pages_float: {
                files: {
                    '../../pages/static/js/pages_float.min.js': '<%= concat.pages_float.dest %>'
                }
            },
            users: {
                files: {
                    '../../users/static/js/users.min.js': '<%= concat.users.dest %>'
                }
            }
        },
        // SASS -> CSS
        sass: {
            dist: {
                files: {
                    'main/css/base.css': 'main/css/base.scss',
                    'main/css/morris.css': 'main/css/morris.scss',
                    'main/css/font-awesome.css': 'main/css/font-awesome.scss',
                    'users/css/styles.css': 'users/css/styles.scss'
                }
            }
        },
        // Сжимаем css
        cssmin: {
            main: {
                src: [
                    'main/css/base.css',
                    'main/css/morris.css',
                    'main/css/font-awesome.css'
                ],
                dest: '../dest/css/main.min.css'
            },
            users: {
                src: ['users/css/styles.css'],
                dest: '../../users/static/css/users.min.css'
            }
        },
        copy: {
            fonts: {
                expand: true,
                cwd: 'main/fonts/',
                src: '**',
                dest: '../dest/fonts/',
                flatten: true
            },
            pages_float: {
                expand: true,
                cwd: 'pages/js/float/',
                src: 'excanvas.min.js',
                dest: '../../pages/static/js/',
                flatten: true
            },
            main_img: {
                expand: true,
                cwd: 'main/img/',
                src: 'default_user.jpg',
                dest: '../dest/img/',
                flatten: true
            }
        },
        // Следим за изменениями
//        watch: {
//            options: {
//                livereload: true
//            },
//            scripts: {
//                files: [
//                    '**/*.js',
//                    '!main/js/_main_.js',
//                    '!users/js/_users_.js',
//                    '!inventory/js/_inventory_.js'
//                ],
//                tasks: ['concat', 'uglify']
//            },
//            sass: {
//                files: ['**/*.scss'],
//                tasks: ['sass']
//            },
//            styles: {
//                files: ['**/*.css'],
//                tasks: ['cssmin']
//            }
//        }
    });
    // Загрузка плагинов, установленных с помощью npm install
    grunt.loadNpmTasks('grunt-contrib-concat');
    grunt.loadNpmTasks('grunt-contrib-uglify');
    grunt.loadNpmTasks('grunt-contrib-sass');
    grunt.loadNpmTasks('grunt-contrib-cssmin');
    grunt.loadNpmTasks('grunt-contrib-copy');
//    grunt.loadNpmTasks('grunt-contrib-watch');
    // Задача по умолчанию
    grunt.registerTask('default', ['concat', 'uglify', 'sass', 'cssmin', 'copy']);
};