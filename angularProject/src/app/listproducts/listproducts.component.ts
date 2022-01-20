import {Component, Input, OnInit} from '@angular/core';
import {ProductService} from "../product.service";
import {Product} from "../product";
import {ActivatedRoute} from "@angular/router";

@Component({
  selector: 'app-listproducts',
  templateUrl: './listproducts.component.html',
  styleUrls: ['./listproducts.component.css']
})
export class ListproductsComponent implements OnInit {

  products_group: Product[][] | undefined;
  all_products: Product[] = [];
  source!: String;

  constructor(private productService: ProductService, private route: ActivatedRoute) { }

  ngOnInit() {

    this.route.data.subscribe(value => {
      this.source = value['source']
      console.log(value)
      console.log(this.source)
      if (this.source == 'dashboard'){
        this.productService.getDashboard().subscribe(products => {
          this.all_products = products;
          this.products_group = this.groupByN(3, this.all_products);
        })
      }
      else if (this.source == 'myproducts'){
        this.productService.getMyProducts().subscribe(products => {
          this.all_products = products;
          this.products_group = this.groupByN(3, this.all_products);
        })
      }

      console.log(this.all_products)
    })

  }
  groupByN(n: number, data: Product[]) {
    console.log("AAAAAAAAA")
    console.log(data)
    let result = [];
    for (let i = 0; i < data.length; i += n) result.push(data.slice(i, i + n));
    console.log(result)
    return result;
  };

}
