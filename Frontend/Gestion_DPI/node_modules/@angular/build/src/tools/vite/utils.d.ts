/**
 * @license
 * Copyright Google LLC All Rights Reserved.
 *
 * Use of this source code is governed by an MIT-style license that can be
 * found in the LICENSE file at https://angular.dev/license
 */
export type AngularMemoryOutputFiles = Map<string, {
    contents: Uint8Array;
    hash: string;
    servable: boolean;
}>;
export declare function pathnameWithoutBasePath(url: string, basePath: string): string;
export declare function lookupMimeTypeFromRequest(url: string): string | undefined;
