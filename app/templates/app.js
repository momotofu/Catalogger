// import app JavaScript
import CategoryList from './category'
import Page from './category/page'
import ItemViewModel from './item'

// set up utilities for cetogories page
import * as categoryPageUtils from './category/utils'

// import vendor js
import * as $ from 'jquery'
import 'bootstrap'
import * as ko from 'knockout'
import '@fortawesome/fontawesome'
import '@fortawesome/fontawesome-free-brands'
import '@fortawesome/fontawesome-free-regular'
import '@fortawesome/fontawesome-free-solid'

// import CSS
import './main.css'

// expose modules to global scope
window.CategoryList = CategoryList
window.categoryPageUtils = categoryPageUtils
window.Page = Page
window.ItemViewModel = ItemViewModel

// expose frameworks to global scope
window.$ = $
window.ko = ko
