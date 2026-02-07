export interface Category {
  id: string;
  name: string;
  description: string;
  parentId: string | null;
  slug: string;
  isActive: boolean;
  sortOrder: number;
  createdAt: Date;
  updatedAt: Date;
}

export interface CreateCategoryDTO {
  name: string;
  description: string;
  parentId?: string;
  sortOrder?: number;
}

export interface UpdateCategoryDTO {
  name?: string;
  description?: string;
  parentId?: string | null;
  isActive?: boolean;
  sortOrder?: number;
}

export interface CategoryTree extends Category {
  children: CategoryTree[];
}

