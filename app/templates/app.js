// import app JavaScript
import CategoryList from './category'
import Page from './category/page'
import CreateItemViewModel from './item'

// import vendor js
import 'bootstrap'
import * as ko from 'knockout'

// import CSS
import './main.css'

// expose modules to global scope
window.CategoryList = CategoryList
window.Page = Page
window.CreateItemViewModel = CreateItemViewModel

// expose frameworks to global scope
window.ko = ko
