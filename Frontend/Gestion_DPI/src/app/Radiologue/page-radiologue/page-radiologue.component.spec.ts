import { ComponentFixture, TestBed } from '@angular/core/testing';

import { PageRadiologueComponent } from './page-radiologue.component';

describe('PageRadiologueComponent', () => {
  let component: PageRadiologueComponent;
  let fixture: ComponentFixture<PageRadiologueComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [PageRadiologueComponent]
    })
    .compileComponents();

    fixture = TestBed.createComponent(PageRadiologueComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
