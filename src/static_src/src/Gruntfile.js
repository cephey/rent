// Обязательная обёртка
module.exports = function (grunt) {
    // Задачи
    grunt.initConfig({
        // Склеиваем
        concat: {
            main: {
                src: [
                    'main/js/*.js', '!main/js/_main_.js'
                ],
                dest: 'main/js/_main_.js'
            },
            users: {
                src: [
                    'users/js/*.js', '!users/js/_users_.js'
                ],
                dest: 'users/js/_users_.js'
            },
            inventory: {
                src: [
                    'inventory/js/*.js', '!inventory/js/_inventory_.js'
                ],
                dest: 'inventory/js/_inventory_.js'
            }
        },
        // Сжимаем js
        uglify: {
            base: {
                files: {
                    '../dest/js/main.min.js': '<%= concat.main.dest %>'
                }
            },
            users: {
                files: {
                    '../../users/static/js/users.min.js': '<%= concat.users.dest %>'
                }
            },
            inventory: {
                files: {
                    '../../inventory/static/js/inventory.min.js': '<%= concat.inventory.dest %>'
                }
            }
        },
        // SASS -> CSS
        sass: {
            dist: {
                files: {
                    'main/css/base.css': 'main/css/base.scss',
                    'users/css/index.css': 'users/css/index.scss',
                    'inventory/css/index.css': 'inventory/css/index.scss'
                }
            }
        },
        // Сжимаем css
        cssmin: {
            main: {
                src: 'main/css/base.css',
                dest: '../dest/css/main.min.css'
            },
            users: {
                src: 'users/css/index.css',
                dest: '../../users/static/css/users.min.css'
            },
            inventory: {
                src: 'inventory/css/index.css',
                dest: '../../inventory/static/css/inventory.min.css'
            }
        },
//        copy: {
//            fonts: {
//                expand: true,
//                cwd: 'bootstrap-3.1.1/fonts/',
//                src: '**',
//                dest: 'fonts/',
//                flatten: true
//            }
//        },
        // Следим за изменениями
        watch: {
            options: {
                livereload: true
            },
            scripts: {
                files: [
                    '**/*.js',
                    '!main/js/_main_.js',
                    '!users/js/_users_.js',
                    '!inventory/js/_inventory_.js'
                ],
                tasks: ['concat', 'uglify']
            },
            sass: {
                files: ['**/*.scss'],
                tasks: ['sass']
            },
            styles: {
                files: ['**/*.css'],
                tasks: ['cssmin']
            }
        }
    });
    // Загрузка плагинов, установленных с помощью npm install
    grunt.loadNpmTasks('grunt-contrib-concat');
    grunt.loadNpmTasks('grunt-contrib-uglify');
    grunt.loadNpmTasks('grunt-contrib-sass');
    grunt.loadNpmTasks('grunt-contrib-cssmin');
//    grunt.loadNpmTasks('grunt-contrib-copy');
    grunt.loadNpmTasks('grunt-contrib-watch');
    // Задача по умолчанию
    grunt.registerTask('default', ['concat', 'uglify', 'sass', 'cssmin']);
};