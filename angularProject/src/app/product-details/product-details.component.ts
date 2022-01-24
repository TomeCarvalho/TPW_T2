import { Component, OnInit } from '@angular/core';
import {ProductService} from "../product.service";
import {Product} from "../product";
import {ActivatedRoute} from "@angular/router";
import {LoginService} from "../login.service";
import {FormBuilder} from "@angular/forms";
import {Router} from "@angular/router";

@Component({
  selector: 'app-product-details',
  templateUrl: './product-details.component.html',
  styleUrls: ['./product-details.component.css']
})
export class ProductDetailsComponent implements OnInit {

  product!: Product;
  fa_icon: string | undefined;
  hidden_toggle_text: string | undefined;
  user: any = localStorage.getItem("username");
  is_superuser: boolean = true;
  num!: number;
  add_to_cartForm = this.formBuilder.group({
    "quantity": ''
  })
  addStockForm = this.formBuilder.group({
    "stockQuantity": ''
  })
  addImgForm = this.formBuilder.group({
    "imageURL": ''
  })
  addGroupForm = this.formBuilder.group({
    "group": ''
  })

  constructor(public loginService: LoginService, private productService: ProductService, private route: ActivatedRoute,
              private formBuilder: FormBuilder, private router: Router) { }

  ngOnInit(): void {
    this.num = +this.route.snapshot.paramMap.get('num')!;
    this.getProduct();
    console.log("USER: "+ this.user)
  }

  getProduct(): void {
    this.productService.getProduct(this.num).subscribe(product => {
      this.product = product
      console.log("FFFFFFFFF");
      console.log(this.product);
      // @ts-ignore
      if(product==404) {
        this.router.navigate(['/dashboard']);
      }
      this.fa_icon = (this.product?.hidden ? 'fa-eye' : 'fa-eye-slash');
      this.hidden_toggle_text = (this.product?.hidden ? 'Unhide Product' : 'Hide Product');
    });
  }

  onAdd_to_cart(data: any): void {
    console.log(data.quantity)
    this.productService.add_to_cart(this.num, data.quantity)
    this.router.navigate(['/cart']);
  }

  onAddStock(data: any): void {
    this.productService.addStock(this.num, data.stockQuantity)
    this.getProduct();
  }

  onAddImg(data: any): void {
    this.productService.addImage(this.num, data.imageURL)
    this.product.images.push(data.imageURL)
  }

  onAddGroup(data: any): void{
    this.productService.addGroup(this.num, data.group)
    this.product.group.push({name: data.group})
  }

  onToggleVis(): void {
    this.productService.toggleVisibility(this.num)
    this.product.hidden = !this.product.hidden
    this.fa_icon = (this.product?.hidden ? 'fa-eye' : 'fa-eye-slash');
    this.hidden_toggle_text = (this.product?.hidden ? 'Unhide Product' : 'Hide Product');
    //location.reload();
  }
}
