'use strict';

/* eslint-env node */

const htmlvalidate = require('gulp-html');
const bs = require('browser-sync');
const gulp = require('gulp');
const colors = require('ansi-colors');

const inputPaths = {
    Css: '*.css',
    Html: '*.html',
};

gulp.task('validatecss', function (done) {
    let status = true;
    bs.reload();
    gulp.src(inputPaths.Css)
        .pipe(htmlvalidate({'Werror': true, 'css': true}))
        .on('error', function (error){
            status = false;
            console.log('============== CSS ==================');
            let nbErrors = 0;
            let nbWarnings = 0;
            const lines = error.message.split('\n');
            lines.forEach(function (line) {
                const parts = line.split(':');
                if (parts.length >= 4) {
                    if (parts[3].trim() === 'error') {
                        console.log(colors.red(line));
                        nbErrors += 1;
                    }
                    else if (parts[3].trim() === 'info warning') {
                        console.log(colors.yellow(line));
                        nbWarnings += 1;
                    }
                    else
                        console.log(line);
                }
            });
            console.log(nbErrors + ' error - ' + nbWarnings + ' warnings\n');
        })
        .on('end', function () {
            if (status === true) {
                console.log('============== CSS ==================');
                console.log(colors.green('No errors or warnings\n'));
            }
        });
    done();
});

gulp.task('validatehtml', function (done) {
    let status = true;
    bs.reload();
    gulp.src(inputPaths.Html)
        .pipe(htmlvalidate({'Werror':true}))
        .on('error', function (error){
            status = false;
            console.log('============== HTML ==================');
            let nbErrors = 0;
            let nbWarnings = 0;
            let lines = error.message.split('\n');
            lines.forEach(function (line) {
                let parts=line.split(':');
                if( parts.length >= 4){
                    if( parts[3].trim() === 'error' ){
                        console.log(colors.red(line));
                        nbErrors++;
                    }
                    else if ( parts[3].trim() === 'info warning' )
                    {
                        console.log(colors.yellow(line));
                        nbWarnings++
                    }
                    else
                        console.log(line);
                }
            });
            console.log(nbErrors + ' error - ' + nbWarnings + ' warnings\n');
        })
        .on('end', function(message) {
            if (status === true) {
                console.log('============== HTML ==================');
                console.log(colors.green('No errors or warnings\n'));
            }
        });
    done();
});

gulp.task('browser-sync', function (done) {
    bs.init({
        server: {
            baseDir: './',
        },
    });
    done();
});

gulp.task('watch', function (done) {
    gulp.watch(inputPaths.Html).on('change', gulp.series('validatehtml'));
    gulp.watch(inputPaths.Css).on('change', gulp.series('validatecss'));
    done();

});

gulp.task('validate', gulp.series('validatehtml', 'validatecss'));

// The default task (called when you run `gulp` from cli)
gulp.task('default', gulp.series('validate', 'watch', 'browser-sync'));

