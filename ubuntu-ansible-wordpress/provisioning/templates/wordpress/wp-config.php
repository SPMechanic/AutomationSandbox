<?php
/**
 * The base configuration for WordPress
 *
 * The wp-config.php creation script uses this file during the
 * installation. You don't have to use the web site, you can
 * copy this file to "wp-config.php" and fill in the values.
 *
 * This file contains the following configurations:
 *
 * * MySQL settings
 * * Secret keys
 * * Database table prefix
 * * ABSPATH
 *
 * @link https://codex.wordpress.org/Editing_wp-config.php
 *
 * @package WordPress
 */

// ** MySQL settings - You can get this info from your web host ** //
/** The name of the database for WordPress */
define('DB_NAME', 'wordpress');

/** MySQL database username */
define('DB_USER', 'wordpress');

/** MySQL database password */
define('DB_PASSWORD', 'bananas');

/** MySQL hostname */
define('DB_HOST', 'localhost');

/** Database Charset to use in creating database tables. */
define('DB_CHARSET', 'utf8mb4');

/** The Database Collate type. Don't change this if in doubt. */
define('DB_COLLATE', '');

/**#@+
 * Authentication Unique Keys and Salts.
 *
 * Change these to different unique phrases!
 * You can generate these using the {@link https://api.wordpress.org/secret-key/1.1/salt/ WordPress.org secret-key service}
 * You can change these at any point in time to invalidate all existing cookies. This will force all users to have to log in again.
 *
 * @since 2.6.0
 */
define('AUTH_KEY',         'TFvwLm&)0rhW?%r@g&R1,`lS9$,k@Kd`O%vZB80p~B~K(LR`p1*AU^?zL nBfF;@');
define('SECURE_AUTH_KEY',  'h%zP:Dzn1,kTH?q )s4h9(BkiMWcp|`2@<Av<eLS:*Y(]X$-9pFLiLIg<%EpV/ei');
define('LOGGED_IN_KEY',    '4qBkzQ XmsAyMSwOn.Jc.@5Zd2?6aDS|b.SwsaJhBkMQcc(a^Pd:/ (n(PEEv>fJ');
define('NONCE_KEY',        '68@~;_pa O^uQo?H~x%$;6]C?=:cK]mT[)UqH,f/MU,AiX.c&5o:J,M|p/wy%yWx');
define('AUTH_SALT',        'P+SIj#Gv,PJM0~hN#IYq0a,^3Wk,1?g=EjcT>wC$e-lFgD*(sRryD:;[ZCx4ToGy');
define('SECURE_AUTH_SALT', 'RdvG~/4t,/#t+fn3EI4RE%4:mL0x8iAj_CmAdGKCe1H<7HmgYT wWjl:YF;BYubY');
define('LOGGED_IN_SALT',   'D]H>5kS4%;1;RUdnBDmST2/Y+(wF$5N#*#D-n`YD:`0wdkz3x^tQKoE.2[Gr/aRM');
define('NONCE_SALT',       '-bjXwVU?j|)]!nuPe6ejE!#gs!:r1H3cPa34Rk#p:;l!P*7TJ~Akm>.^V=9n]`_D');

/**#@-*/

/**
 * WordPress Database Table prefix.
 *
 * You can have multiple installations in one database if you give each
 * a unique prefix. Only numbers, letters, and underscores please!
 */
$table_prefix  = 'wp_';

/**
 * For developers: WordPress debugging mode.
 *
 * Change this to true to enable the display of notices during development.
 * It is strongly recommended that plugin and theme developers use WP_DEBUG
 * in their development environments.
 *
 * For information on other constants that can be used for debugging,
 * visit the Codex.
 *
 * @link https://codex.wordpress.org/Debugging_in_WordPress
 */
define('WP_DEBUG', false);

/* That's all, stop editing! Happy blogging. */

/** Absolute path to the WordPress directory. */
if ( !defined('ABSPATH') )
	define('ABSPATH', dirname(__FILE__) . '/');

/** Sets up WordPress vars and included files. */
require_once(ABSPATH . 'wp-settings.php');

