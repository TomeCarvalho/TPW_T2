import { Component, OnInit } from '@angular/core';
import {FormBuilder} from "@angular/forms";
import {ProductService} from "../product.service";
import {Router} from "@angular/router";

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

  constructor(private formBuilder: FormBuilder, private productService: ProductService, private router: Router) {
    if(localStorage.getItem('loginToken') == ''){
      router.navigate(['dashboard'])
    }
  }

  ngOnInit(): void {
  }

  onSubmit(data: any) {
    this.productService.addProduct(data).then(
      () => {
        this.router.navigate(['myproducts'])
      },
      () => {
        this.productForm.reset()
      }
    );
  }

}
