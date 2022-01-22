import { Component, OnInit } from '@angular/core';
import {FormBuilder} from "@angular/forms";
import {ListproductsComponent} from "../listproducts/listproducts.component";
import {ProductService} from "../product.service";
import {Router} from "@angular/router";

@Component({
  selector: 'app-filter',
  templateUrl: './filter.component.html',
  styleUrls: ['./filter.component.css']
})
export class FilterComponent implements OnInit {

  groups: any = [];

  order = [
    {name: "Alphabetical ↑", value: "name"},
    {name: "Alphabetical ↓", value: "-name"},
    {name: "Category ↑", value: "category"},
    {name: "Category ↓", value: "-category"},
    {name: "Group ↑", value: "group"},
    {name: "Group ↓", value: "-group"},
    {name: "Price ↑", value: "price"},
    {name: "Price ↓", value: "-price"}
  ]

  filterForm = this.formBuilder.group({
    group: '',
    category: '',
    upper: '',
    lower: '',
    order: '',
  })


  constructor(private listProduct: ListproductsComponent,
              private formBuilder: FormBuilder,
              private productService: ProductService,
              private router: Router) { }

  ngOnInit(): void {
    this.productService.getGroups().subscribe(
      value => {
        for(let group of value){
          console.log(group.name)
          this.groups.push({name: group.name, value: group.name})
        }
      }
    )
  }

  onSubmit(data: any) {
    let queryParam: any = {}
    for (let [key, value] of Object.entries(data)) {
      if (value) {
        console.log(value)
        queryParam[key] = value}
      }
    console.log(queryParam)
    this.router.navigate([this.router.url.split('?')[0] ], { queryParams: queryParam})
  }
}
