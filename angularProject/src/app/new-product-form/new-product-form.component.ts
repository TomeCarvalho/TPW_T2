import { Component, OnInit } from '@angular/core';
import {FormBuilder} from "@angular/forms";
import {ProductService} from "../product.service";

@Component({
  selector: 'app-new-product-form',
  templateUrl: './new-product-form.component.html',
  styleUrls: ['./new-product-form.component.css']
})
export class NewProductFormComponent implements OnInit {

  productForm = this.formBuilder.group({
    group: '',
    category: '',
    name: '',
    price: '',
    stock: '',
    image: '',
    description: ''
  })

  constructor(private formBuilder: FormBuilder, private productService: ProductService) { }

  ngOnInit(): void {
  }

  onSubmit(data: any) {
    this.productService.addProduct(data);
  }

}
