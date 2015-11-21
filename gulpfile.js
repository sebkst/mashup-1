var gulp = require('gulp'),
  gulp_jspm = require('gulp-jspm'),
  uglify = require('gulp-uglify'),
  minify = require('gulp-minify'),
  del = require('del'),
  shell = require('gulp-shell'),
  htmlreplace = require('gulp-html-replace'),
  runSequence = require('run-sequence'),
  sass = require('gulp-ruby-sass'),
  sourcemaps = require('gulp-sourcemaps'),
  connect = require('gulp-connect');

////////////////////////////////////////////////////////////////////////////////
//  UTILS
////////////////////////////////////////////////////////////////////////////////
gulp.task('clean', function() {
    return del(['dist/*']);
});
////////////////////////////////////////////////////////////////////////////////
//  LIVE SERVER
////////////////////////////////////////////////////////////////////////////////
// Html task
gulp.task('rhtml', function() {
  gulp.src('./app/*.html')
  .pipe(connect.reload());
});

//Js task
gulp.task('rjs', function() {
  gulp.src('./app/**/*.js')
  .pipe(connect.reload());
});

//Reload sass compiled css
gulp.task('rcss', ['sass'],function () {
    gulp.src('./app/assets/css/*.css')
    .pipe(connect.reload());
});

// Watch our changes
gulp.task('watch', function(){
  //html
  gulp.watch(['./app/*.html'], ['rhtml']);
  gulp.watch(['./app/**/*.html'], ['rhtml']);
  gulp.watch(['./app/**/*.js'], ['rjs']);
  gulp.watch(['./app/assets/sass/*.scss'],['rcss'])
});

gulp.task('connect', function() {
  connect.server({
    root: './app/',
    livereload: true
  });
});

////////////////////////////////////////////////////////////////////////////////
//  BUILD
////////////////////////////////////////////////////////////////////////////////
gulp.task('sass', function () {
    console.log('ok')
    return sass('app/assets/sass/*.scss', {sourcemap: false})
        .on('error', function (err) {
            console.error('Error!', err.message);
        })
        .pipe(sourcemaps.write('maps', {
            includeContent: false
        }))
        .pipe(gulp.dest('./app/assets/css'));
});

gulp.task('js', function(){
    return gulp.src('app/src/boot.js')
    .pipe(shell([
      'jspm bundle-sfx app/boot ../dist/js/bundle.min.js --minify --skip-source-maps'],{cwd:'app/'}));
});

// Views task
gulp.task('html',function() {
  // Get our index.html
  gulp.src('app/index.html')
  .pipe(htmlreplace({
        'js': 'js/bundle.min.js'
    }))
  // And put it in the dist folder
  .pipe(gulp.dest('dist/'));

  // Any other view files from app/views
  gulp.src('./app/views/**/*')
  // Will be put in the dist/views folder
  .pipe(gulp.dest('dist/views/'));
});

// images task
gulp.task('images',function() {
  // Any other view files from app/views
  gulp.src('./app/assets/images/**/*')
  // Will be put in the dist/views folder
  .pipe(gulp.dest('dist/assets/images/'));
});

// images task
gulp.task('css',['sass'],function() {
  // Any other view files from app/views
  gulp.src('./app/assets/css/**/*')
  // Will be put in the dist/views folder
  .pipe(gulp.dest('dist/assets/css/'));
});


//Build sequence
gulp.task('build', function(){
    return runSequence('clean','js', 'css','images', 'html');
});
////////////////////////////////////////////////////////////////////////////////
//  RSYNC
////////////////////////////////////////////////////////////////////////////////
var rsync = require('gulp-rsync');

gulp.task('push',function(){

    return gulp.src('dist/**/*.*')
        .pipe(rsync({
            root: 'dist',
            username: 'qwhack',
            recursive: true,
            clean: true,
            hostname: 'qwhack.xyz',
            destination: '/var/www/qWhack/frontend/static_content/'
        }));

});
////////////////////////////////////////////////////////////////////////////////
//  DEFAULT
////////////////////////////////////////////////////////////////////////////////

// Start the tasks
gulp.task('default', ['connect','watch']);
gulp.task('we',['watch']);
