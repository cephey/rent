// Обязательная обёртка
module.exports = function (grunt) {
    // Задачи
    grunt.initConfig({
        // Склеиваем
        concat: {
            common: {
                src: [
                    'js_src/base.js'
                ],
                dest: 'js/base.js'
            },
            users: {
                src: [
                    '../users/static/js/*.js'
                ],
                dest: 'js/users.js'
            }
        },
        // Сжимаем js
        uglify: {
            base: {
                files: {
                    'js/base.min.js': '<%= concat.base.dest %>'
                }
            },
            users: {
                files: {
                    'js/users.min.js': '<%= concat.users.dest %>'
                }
            }
        },
        // SASS -> CSS
        sass: {
            dist: {
                files: {
                    'css/base.css': 'css_src/base.scss',
                    'css/index.css': 'css_src/index.scss',
                    'css/login.css': 'css_src/login.scss',
                    'css/pattern.css': 'css_src/pattern.scss'
                }
            }
        },
        // Сжимаем css
        cssmin: {
            base: {
                src: 'css/base.css',
                dest: 'css/base.min.css'
            },
            index: {
                src: 'css/index.css',
                dest: 'css/index.min.css'
            },
            login: {
                src: 'css/login.css',
                dest: 'css/login.min.css'
            },
            pattern: {
                src: 'css/pattern.css',
                dest: 'css/pattern.min.css'
            }
        },
        copy: {
            fonts: {
                expand: true,
                cwd: 'bootstrap-3.1.1/fonts/',
                src: '**',
                dest: 'fonts/',
                flatten: true
            }
        },
        // Следим за изменениями
        watch: {
            scripts: {
                files: [
                    'js_src/*.js',
                    '../account/static/js/*.js',
                    '../pages/static/js/*.js'
                ],
                tasks: ['concat', 'uglify'],
                options: {
                    spawn: false
                }
            }
        }
    });
    // Загрузка плагинов, установленных с помощью npm install
    grunt.loadNpmTasks('grunt-contrib-concat');
    grunt.loadNpmTasks('grunt-contrib-uglify');
    grunt.loadNpmTasks('grunt-contrib-sass');
    grunt.loadNpmTasks('grunt-contrib-cssmin');
    grunt.loadNpmTasks('grunt-contrib-copy');
    grunt.loadNpmTasks('grunt-contrib-watch');
    // Задача по умолчанию
    grunt.registerTask('default', ['concat', 'uglify', 'sass', 'cssmin', 'copy']);
};