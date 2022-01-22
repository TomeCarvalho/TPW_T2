import { Component, OnInit } from '@angular/core';
import {ProductService} from "../product.service";
import {Product} from "../product";
import {ActivatedRoute} from "@angular/router";
import {LoginService} from "../login.service";

@Component({
  selector: 'app-product-details',
  templateUrl: './product-details.component.html',
  styleUrls: ['./product-details.component.css']
})
export class ProductDetailsComponent implements OnInit {

  product!: Product;
  fa_icon: string | undefined;
  hidden_toggle_text: string | undefined;
  user: number = 1;
  is_superuser: boolean = false;
  num!: number;

  constructor(public loginService: LoginService, private productService: ProductService, private route: ActivatedRoute) { }

  ngOnInit(): void {
    this.num = +this.route.snapshot.paramMap.get('num')!;
    this.getProduct();
    this.fa_icon = (this.product?.hidden ? 'fa-eye' : 'fa-eye-slash');
    this.hidden_toggle_text = (this.product?.hidden ? 'Unhide Product' : 'Hide Product');
  }

  getProduct(): void {
    this.productService.getProduct(this.num).subscribe(product => this.product = product);
  }

}
