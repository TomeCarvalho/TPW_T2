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
  source!: string;

  constructor(private productService: ProductService, private route: ActivatedRoute) { }

  ngOnInit() {

    this.route.data.subscribe(value => {
      this.source = value['source']
      this.getProducts("");
    })

  }

  getProducts(query: string){
    this.productService.getProducts(this.source, query).subscribe(products => {
      this.all_products = products;
      this.products_group = this.groupByN(3, this.all_products);
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
