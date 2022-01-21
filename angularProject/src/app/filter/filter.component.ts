import { Component, OnInit } from '@angular/core';
import {FormBuilder} from "@angular/forms";
import {ListproductsComponent} from "../listproducts/listproducts.component";
import {ProductService} from "../product.service";

@Component({
  selector: 'app-filter',
  templateUrl: './filter.component.html',
  styleUrls: ['./filter.component.css']
})
export class FilterComponent implements OnInit {

  // TODO: add fetch of groups in api
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
              private productService: ProductService) { }

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
    let query = "?";
    console.log(data)
    for (let [key, value] of Object.entries(data)) {
      if (value) {
        console.log(value)
        query += `${key}=${value}&`;
      }
    }
    console.log(query)
    this.listProduct.getProducts(query);
  }
}
